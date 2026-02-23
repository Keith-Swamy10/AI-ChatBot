import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql

# Load environment variables
load_dotenv()

# Import your routers
from app.api import leads
from app.leads.lead_extractor import process_lead_input
from app.leads.lead_state_service import should_start_lead_flow, detect_lead_signal, detect_opportunistic_contact, update_lead_state, get_or_create_lead_state, count_user_messages, store_intent_summary
from app.core.config import get_settings

# FastAPI App Setup
app = FastAPI(title="AI Chatbot Backend")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TEMP - lock this down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, prefix="/api", tags=["Leads"])

@app.get("/")
def root():
    return {"message": "Welcome to AI Chatbot Backend!", "status": "running"}


def get_db_connection():
    settings = get_settings()
    return pymysql.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name
    )


def save_chat_message(session_id: str, message: str, sender: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        try:
            cursor.execute(
                """
                INSERT INTO chats (session_id, message, sender, timestamp)
                VALUES (%s, %s, %s, NOW())
                """,
                (session_id, message, sender)
            )
        except pymysql.err.OperationalError as e:
            # Support schemas where chats table does not have a timestamp column.
            if e.args and e.args[0] == 1054:
                cursor.execute(
                    """
                    INSERT INTO chats (session_id, message, sender)
                    VALUES (%s, %s, %s)
                    """,
                    (session_id, message, sender)
                )
            else:
                raise
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def retrieve_chats(session_id: str, limit: int = 20):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT message, sender FROM chats
            WHERE session_id = %s
            ORDER BY id DESC
            LIMIT %s
            """,
            (session_id, limit)
        )
        rows = cursor.fetchall()
        return [{"message": row[0], "sender": row[1]} for row in rows]
    finally:
        cursor.close()
        conn.close()


def append_name_request(answer: str) -> str:
    prompt = "Before we continue, may I know your name?"
    if not answer:
        return prompt
    return f"{answer}\n\n{prompt}"


# ===================================================================
# INTEGRATED CHAT ENDPOINT (Lead Capture + PDF/Azure)
# ===================================================================
class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    lead_completed: bool = False
    is_lead_flow: bool = False


AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Try to load PDFs and set up Azure
vector_store = None
retriever = None
llm = None
embeddings_setup = False

if AZURE_OPENAI_ENDPOINT and OPENAI_API_KEY:
    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.vectorstores import FAISS
        from langchain_core.prompts import PromptTemplate
        from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI

        # Load PDFs if available
        folder_path = "pdfs"
        docs = []
        if os.path.exists(folder_path) and os.listdir(folder_path):
            for file in os.listdir(folder_path):
                if file.lower().endswith(".pdf"):
                    try:
                        pdf_path = os.path.join(folder_path, file)
                        loader = PyPDFLoader(pdf_path)
                        docs.extend(loader.load())
                        print(f"✓ Loaded PDF: {file}")
                    except Exception as e:
                        print(f"✗ Error loading {file}: {e}")

        if docs:
            print(f"✓ Found {len(docs)} document pages")
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=OPENAI_API_KEY,
                deployment="text-embedding-3-small",
                api_version="2024-12-01-preview"
            )

            vector_store = FAISS.from_documents(chunks, embeddings)
            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
            embeddings_setup = True
            print("✓ Vector store ready")

        llm = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=OPENAI_API_KEY,
            deployment_name="o3-mini",
            api_version="2024-12-01-preview",
        )
        
    except Exception as e:
        print(f"⚠️  Error setting up Azure: {e}")
        llm = None


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Integrated chat endpoint that handles:
    1. Lead capture (email, phone, names, lead signals)
    2. PDF-based Q&A (if PDFs available)
    3. Fallback responses for generic questions
    """
    user_message = request.message.strip()
    session_id = request.session_id

    if not user_message:
        raise HTTPException(status_code=400, detail="Empty message")

    print(f"\n[CHAT] Session: {session_id}, Message length: {len(user_message)}")

    # Persist user messages so proactive lead rules can use message count.
    try:
        save_chat_message(session_id, user_message, "user")
    except Exception as e:
        print(f"[CHAT] Could not persist user message: {e}")

    # ===================================
    # 0. CHECK FOR STRONG LEAD SIGNALS FIRST
    # ===================================
    # Even if in COMPLETED state, strong signals should restart lead flow
    
    append_name_at_end = False

    try:
        has_opportunistic = detect_opportunistic_contact(user_message)
        has_keyword_signal = detect_lead_signal(user_message)
        has_strong_signal = has_opportunistic or has_keyword_signal
        
        print(f"[LEAD] Strong signal check: opportunistic={has_opportunistic}, keyword={has_keyword_signal}, combined={has_strong_signal}")
        
        current_state = get_or_create_lead_state(session_id)
        print(f"[LEAD] Current state: {current_state}")
        
        # If lead is already completed, don't restart the flow
        if current_state == "COMPLETED":
            print(f"[LEAD] Lead already completed - skipping lead flow")
            # Fall through directly to Azure/PDF chat

        # ===================================
        # 1. CHECK LEAD STATE
        # ===================================
        proactive_triggered_this_turn = False
        
        # Check if we should start lead flow (only if currently NONE)
        if current_state == "NONE":
            user_turns = count_user_messages(session_id)
            proactive_candidate = (not has_strong_signal) and (user_turns >= 4)

            if proactive_candidate:
                print(f"[LEAD] Proactive threshold reached at {user_turns} user messages")
                update_lead_state(session_id, "ASKED_NAME")
                store_intent_summary(session_id, "User showed sustained interest after multiple messages")
                current_state = "ASKED_NAME"
                proactive_triggered_this_turn = True
                append_name_at_end = True
                print("[LEAD] Proactive trigger: answer question first, append name request")
            else:
                should_start = should_start_lead_flow(session_id, user_message)
                print(f"[LEAD] Should start lead flow: {should_start}")
                if should_start:
                    # State was updated by should_start_lead_flow
                    current_state = get_or_create_lead_state(session_id)
                    print(f"[LEAD] State updated to: {current_state}")
        
        # ===================================
        # 2. PROCESS LEAD FLOW IF ACTIVE
        # ===================================
        if current_state != "NONE" and not proactive_triggered_this_turn:
            print(f"[LEAD] Processing lead input in state: {current_state}")
            # We're in lead flow, process the input
            result = process_lead_input(session_id, user_message)
            print(f"[LEAD] Result: handled={result['handled']}, lead_completed={result.get('lead_completed', False)}, message={result['message'][:50] if result['message'] else None}")
            if result["handled"]:
                return ChatResponse(
                    answer=result["message"],
                    lead_completed=result.get("lead_completed", False),
                    is_lead_flow=True
                )
            print(f"[LEAD] Lead input not handled, falling through to Azure/PDF")
    except Exception as e:
        # Keep chatbot available even if lead/DB pipeline is down.
        print(f"[LEAD] Lead pipeline error. Continuing with chat fallback. Error: {e}")

    # ===================================
    # 3. TRY PDF/AZURE CHAT
    # ===================================
    print(f"[CHAT] Trying Azure/PDF (embeddings_setup={embeddings_setup})")
    if embeddings_setup and retriever and llm:
        try:
            retrieved_docs = retriever.invoke(user_message)
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

            # Get previous chat history
            previous_chats = retrieve_chats(session_id, 20)
            previous_chat_context = "\n".join(
                f"{chat['sender']}: {chat['message']}"
                for chat in reversed(previous_chats)
            )

            lead_step = get_or_create_lead_state(session_id)

            chat_prompt = PromptTemplate(
                template="""
You are a helpful company assistant that answers user questions based on the provided context.

CURRENT_LEAD_STEP: {lead_step}

Guidelines:
- If CURRENT_LEAD_STEP is ASK_NAME:
  Politely ask the user for their name.
- If CURRENT_LEAD_STEP is ASK_EMAIL:
  Politely ask the user for their email address.
- If CURRENT_LEAD_STEP is ASK_PHONE:
  Politely ask the user for their phone number.
- If CURRENT_LEAD_STEP is NONE or COMPLETED:
  Answer the user's question using the provided context and previous chats.

Please ask for only one detail at a time and follow the order above.
Please avoid mentioning lead collection to the user.

Context:
{context}

Previous Chats:
{previous_20}

User Question:
{question}
""",
                input_variables=["context", "question", "previous_20", "lead_step"]
            )

            final_prompt = chat_prompt.invoke({
                "context": context_text,
                "question": user_message,
                "previous_20": previous_chat_context,
                "lead_step": lead_step
            })

            response = llm.invoke(final_prompt)
            answer_text = str(response.content)
            if append_name_at_end:
                answer_text = append_name_request(answer_text)

            print(f"[CHAT] Azure response: {answer_text}")
            try:
                save_chat_message(session_id, answer_text, "ai")
            except Exception as e:
                print(f"[CHAT] Could not persist AI message: {e}")
            return ChatResponse(answer=answer_text, is_lead_flow=False)
        except Exception as e:
            print(f"[ERROR] Azure error: {e}")
            # Fall through to generic response
    
    # ===================================
    # 4. FALLBACK GENERIC RESPONSES
    # ===================================
    print(f"[CHAT] Using fallback responses")
    fallback_responses = {
        "hi": "Hello! How can I help you today? Feel free to ask me questions or let us know if you'd like to get in touch.",
        "hello": "Hi there! What can I help you with?",
        "help": "I'm here to answer your questions! You can also ask about our services, pricing, or contact us if interested.",
        "thanks": "You're welcome! Is there anything else I can help with?",
        "thank you": "My pleasure! Let me know if you need anything else.",
    }

    user_lower = user_message.lower()
    for key, response in fallback_responses.items():
        if key in user_lower:
            print(f"[CHAT] Fallback match: {key}")
            answer_text = append_name_request(response) if append_name_at_end else response
            try:
                save_chat_message(session_id, answer_text, "ai")
            except Exception as e:
                print(f"[CHAT] Could not persist AI message: {e}")
            return ChatResponse(answer=answer_text, is_lead_flow=False)

    # Default fallback
    print(f"[CHAT] Default fallback")
    default_answer = "I'm not sure how to answer that. Could you ask something more specific, or would you like to provide your contact information?"
    answer_text = append_name_request(default_answer) if append_name_at_end else default_answer
    try:
        save_chat_message(session_id, answer_text, "ai")
    except Exception as e:
        print(f"[CHAT] Could not persist AI message: {e}")

    return ChatResponse(
        answer=answer_text,
        is_lead_flow=False
    )


# ===================================================================
# Health Check Endpoint
# ===================================================================
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Chatbot Backend"}


# ---------------------------------------------------
# SERVE CHATBOT WIDGET JS
# ---------------------------------------------------
CHATBOT_JS_PATH = os.path.join(os.path.dirname(__file__), "chatbot.js")

@app.get("/chatbot.js")
def serve_chatbot_widget():
    if not os.path.exists(CHATBOT_JS_PATH):
        raise HTTPException(status_code=404, detail="chatbot.js not found")
    return FileResponse(CHATBOT_JS_PATH, media_type="application/javascript")
