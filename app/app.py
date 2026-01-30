# from fastapi import FastAPI
# from app.core.config import get_settings
# from app.core.logger import get_logger
# from app.api import chat, leads

# settings = get_settings()
# logger = get_logger()

# app = FastAPI(title=settings.app_name)

# # Routers
# app.include_router(chat.router, prefix="/api", tags=["Chat"])
# app.include_router(leads.router, prefix="/api", tags=["Leads"])

# @app.get("/")
# def root():
#     logger.info("Root endpoint hit")
#     return {"message": f"Welcome to {settings.app_name}!"}


import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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
# REQUEST / RESPONSE MODELS
# ---------------------------------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str


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

# ---------------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------------
folder_path = "pdfs" 
docs = load_pdfs_from_folder(folder_path)

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
Answer ONLY using the provided PDF context.
If the context is insufficient, reply: "I don't know."
Also, If you feel the conversation have end then ask for the email id and phone number from user (Note: Only ask user for the email id and phone number when you feel that the user is satisfied and has no more questions). Also ask the followup similar questions by using your creativity which can be engaging for user based on context.

Context:
{context}

Question: {question}
""",
    input_variables=['context', 'question']
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

    # 1. Retrieve relevant docs
    retrieved_docs = retriever.invoke(user_question)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # 2. Build prompt
    final_prompt = prompt.invoke({
        "context": context_text,
        "question": user_question
    })

    # 3. Call LLM
    try:
        response = llm.invoke(final_prompt)
        return ChatResponse(answer=response.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
