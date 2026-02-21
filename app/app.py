import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

# Load environment variables
load_dotenv()

# Import your routers
from app.api import leads
from app.leads.lead_extractor import process_lead_input
from app.leads.lead_state_service import should_start_lead_flow, detect_lead_signal, detect_opportunistic_contact, update_lead_state, store_intent_summary

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

    print(f"\n[CHAT] Session: {session_id}, Message: {user_message}")

    # ===================================
    # 0. CHECK FOR STRONG LEAD SIGNALS FIRST
    # ===================================
    # Even if in COMPLETED state, strong signals should restart lead flow
    from app.leads.lead_state_service import get_or_create_lead_state
    
    has_opportunistic = detect_opportunistic_contact(user_message)
    has_keyword_signal = detect_lead_signal(user_message)
    has_strong_signal = has_opportunistic or has_keyword_signal
    
    print(f"[LEAD] Strong signal check: opportunistic={has_opportunistic}, keyword={has_keyword_signal}, combined={has_strong_signal}")
    
    current_state = get_or_create_lead_state(session_id)
    print(f"[LEAD] Current state: {current_state}")
    
    # If we have a strong signal and are in COMPLETED state, reset to ask for name again
    if has_strong_signal and current_state == "COMPLETED":
        print(f"[LEAD] Strong signal detected in COMPLETED state - resetting to ASKED_NAME")
        update_lead_state(session_id, "ASKED_NAME")
        # Don't store new intent - original intent is already saved
        current_state = "ASKED_NAME"

    # ===================================
    # 1. CHECK LEAD STATE
    # ===================================
    
    # Check if we should start lead flow (only if currently NONE)
    if current_state == "NONE":
        should_start = should_start_lead_flow(session_id, user_message)
        print(f"[LEAD] Should start lead flow: {should_start}")
        if should_start:
            # State was updated by should_start_lead_flow
            current_state = get_or_create_lead_state(session_id)
            print(f"[LEAD] State updated to: {current_state}")
    
    # ===================================
    # 2. PROCESS LEAD FLOW IF ACTIVE
    # ===================================
    if current_state != "NONE":
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

    # ===================================
    # 3. TRY PDF/AZURE CHAT
    # ===================================
    print(f"[CHAT] Trying Azure/PDF (embeddings_setup={embeddings_setup})")
    if embeddings_setup and retriever and llm:
        try:
            retrieved_docs = retriever.invoke(user_message)
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

            prompt = PromptTemplate(
                template="""
You are a helpful company assistant.
Answer the user's question using ONLY the provided context.
If the context doesn't contain relevant information, say "I don't have that information in my knowledge base."
Be friendly and helpful.

Context:
{context}

Question: {question}
""",
                input_variables=['context', 'question']
            )

            final_prompt = prompt.invoke({
                "context": context_text,
                "question": user_message
            })

            response = llm.invoke(final_prompt)
            print(f"[CHAT] Azure response: {response.content}")
            return ChatResponse(answer=response.content, is_lead_flow=False)
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
            return ChatResponse(answer=response, is_lead_flow=False)

    # Default fallback
    print(f"[CHAT] Default fallback")
    return ChatResponse(
        answer="I'm not sure how to answer that. Could you ask something more specific, or would you like to provide your contact information?",
        is_lead_flow=False
    )


# ===================================================================
# Health Check Endpoint
# ===================================================================
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Chatbot Backend"}
