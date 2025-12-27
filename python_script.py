import os
from dotenv import load_dotenv

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
    print("No PDFs found in folder!")
    exit()

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
# 2. USER QUESTION
# ---------------------------------------------------
question ="What is the company’s dress code?"    # <-- change later

retrieved_docs = retriever.invoke(question)
context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

# ---------------------------------------------------
# 3. LLM PROMPT (same format as your code)
# ---------------------------------------------------
prompt = PromptTemplate(
    template="""
You are a helpful company assistant.
Answer ONLY using the provided PDF context.
If the context is insufficient, reply: "I don't know."

Context:
{context}

Question: {question}
""",
    input_variables=['context', 'question']
)

# Build final prompt for LLM
final_prompt = prompt.invoke({"context": context_text, "question": question})

# ---------------------------------------------------
# 4. CALL LLM (same as your version)
# ---------------------------------------------------
llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=OPENAI_API_KEY,
    deployment_name="o3-mini",  # <-- YOUR chat deployment
    api_version="2024-12-01-preview",
)

answer = llm.invoke(final_prompt)

# ---------------------------------------------------
# 5. PRINT ANSWER
# ---------------------------------------------------
print("\n========== ANSWER ==========")
print(answer.content)
print("End")
print("============================\n")
