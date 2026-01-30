import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---- Install required packages ----
# !pip install -q langchain-community langchain-openai langchain-text-splitters \
#                faiss-cpu pypdf python-dotenv tiktoken

# ---- Imports (latest LangChain structure) ----
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.document_loaders import BSHTMLLoader

if not AZURE_OPENAI_ENDPOINT or not OPENAI_API_KEY:
    raise RuntimeError("Missing Azure OpenAI environment variables")

# ---------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------
app = FastAPI(title="AI Chatbot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TEMP (lock this down later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Update with your MySQL host
            user="root",       # Update with your MySQL username
            password="Saket@123",  # Update with your MySQL password
            database="chatbot_db"  # Update with your database name
        )
        return connection
    except Error as e:
        raise RuntimeError(f"Error connecting to MySQL: {e}")

# ---------------------------------------------------
# REQUEST / RESPONSE MODELS
# ---------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str

# ---------------------------------------------------
# SAVE CHAT FUNCTION
# ---------------------------------------------------
def save_chat(session_id: str, message: str, sender: str):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO chats (session_id, message, sender, timestamp)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (session_id, message, sender, datetime.now()))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

# ---------------------------------------------------
# RETRIEVE CHATS FUNCTION
# ---------------------------------------------------
def retrieve_chats(session_id: str, k: int):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT message, sender FROM chats
        WHERE session_id = %s
        ORDER BY timestamp DESC
        LIMIT %s
        """
        cursor.execute(query, (session_id, k))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

# ---------------------------------------------------
# 1. LOAD ALL DOCUMENTS FROM PDF FOLDER
# ---------------------------------------------------
def load_pdfs_from_folder(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)
            loader = PyPDFLoader(pdf_path)
            docs.extend(loader.load())

    return docs

def load_htmls_from_folder(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(".html"):
            html_path = os.path.join(folder_path, file)
            loader = BSHTMLLoader(html_path)
            docs.extend(loader.load())

    return docs

# ---------------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------------
# folder_path = "pdfs" 
# docs = load_pdfs_from_folder(folder_path)
folder_path = "./data/index_pages_dir"
docs = load_htmls_from_folder(folder_path)

if not docs:
    raise RuntimeError("No PDFs found in pdfs/ folder")

# Convert PDF docs into text chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
# print(chunks)
# for chunk in chunks:
#     print(chunk)

# Create embeddings using OpenAI
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=OPENAI_API_KEY,
    deployment="text-embedding-3-small",  # <-- Azure embedding deployment
    api_version="2024-12-01-preview"
)

# Create vector store
vector_store = FAISS.from_documents(chunks, embeddings)

# Retrieval setup
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# ---------------------------------------------------
# 3. LLM PROMPT (same format as your code)
# ---------------------------------------------------
prompt = PromptTemplate(
    template="""
You are a helpful company assistant.
Answer ONLY using the provided PDF context and previous chats.
If the context and previous chats are insufficient, reply: "I don't know."
Also, If you feel the conversation have ended then ask for the email id and phone number from user (Note: Only ask user for the email id and phone number when you feel that the user is satisfied and has no more questions). Also ask the followup similar questions by using your creativity which can be engaging for user based on context.
If user is asking question related to previous conversations then try to answer using the previous chats.

Context:
{context}

Previous Chats:
{previous_20}

Question: {question}
""",
    input_variables=['context', 'question', 'previous_20']
)

# Define the prompt template
intent_prompt = PromptTemplate(
    template="""
    You are an advanced AI assistant specializing in user intent analysis for businesses.

Analyze the following user chat messages and infer the user intent based only on the provided conversation, without assumptions.

Your task is to summarize the user intent clearly and structurally by answering the following:

User Interest

Is the user interested in the company or its offerings?

If yes, describe the level and nature of interest (exploratory, evaluative, transactional, partnership, etc.).

Segment / Product / Service of Interest

Identify the specific segment(s), product(s), or service(s) the user is interested in (e.g., credit cards, loans, advisory roles, content, support).

User Actual Requirement

Clearly state what the user is ultimately trying to achieve or understand.

What the User Is Looking for That Is Not Present in the Company

Identify any expectations, roles, features, or services implied by the user that may not currently exist in the company.

What the User Is Looking for That Is Present in the Company

Identify offerings, information, or services that align with the user queries and are likely already available.

Additional Intent Insights

Any notable behavioral signals (trust-building, comparison, research phase, partnership intent, credibility checks, etc.).

Output Requirements:

Use clear headings and bullet points.

Be concise, structured, and business-ready.

Do not add external assumptions or hallucinated details.

Base conclusions strictly on the chat content.

    User Chats:
    {user_chats}

    Provide a detailed summary of the user's intent in a structured format.
    """,
    input_variables=['user_chats']
)

# ---------------------------------------------------
# 4. CALL LLM (same as your version)
# ---------------------------------------------------
llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=OPENAI_API_KEY,
    deployment_name="o3-mini",  # <-- YOUR chat deployment
    api_version="2024-12-01-preview",
)

# ---------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_question = request.message.strip()

    if not user_question:
        raise HTTPException(status_code=400, detail="Empty question")

    # Save user question
    save_chat(request.session_id, user_question, "user")

    # Retrieve last 10 chats
    previous_chats = retrieve_chats(request.session_id, 20)
    previous_chat_context = "\n".join(
        f"{chat['sender']}: {chat['message']}" for chat in previous_chats
    )
    print(previous_chat_context)
    # 1. Retrieve relevant docs
    retrieved_docs = retriever.invoke(user_question)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # 2. Build prompt
    final_prompt = prompt.invoke({
        "context": context_text,
        "question": user_question,
        "previous_20": previous_chat_context
    })

    # 3. Call LLM
    try:
        response = llm.invoke(final_prompt)
        ai_response = response.content

        # Save AI response
        save_chat(request.session_id, ai_response, "ai")

        return ChatResponse(answer=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------
# RETRIEVE CHATS ENDPOINT
# ---------------------------------------------------
@app.get("/chats/{session_id}")
def get_chats(session_id: str, k: int = 10):
    try:
        chats = retrieve_chats(session_id, k)
        return {"chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------
# PREDICT INTENT ENDPOINT
# ---------------------------------------------------
@app.get("/predict_intent/{session_id}")
def predict_intent_api(session_id: str):
    try:
        # Retrieve user chats (only user messages)
        user_chats = retrieve_chats(session_id, k=50)
        user_only_chats = [chat['message'] for chat in user_chats if chat['sender'] == 'user']
        user_chat_context = "\n".join(user_only_chats)

        # Build the final prompt
        final_prompt = intent_prompt.invoke({
            "user_chats": user_chat_context
        })

        response = llm.invoke(final_prompt)
        return {"intent_summary": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))