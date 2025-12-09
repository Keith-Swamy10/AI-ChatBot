import os
from dotenv import load_dotenv

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

print(os.getenv("OPENAI_API_KEY"))

# ---- Install required packages ----
# !pip install -q langchain-community langchain-openai langchain-text-splitters \
#                faiss-cpu pypdf python-dotenv tiktoken

# ---- Imports (latest LangChain structure) ----
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate


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
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create vector store
vector_store = FAISS.from_documents(chunks, embeddings)

# Retrieval setup
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# ---------------------------------------------------
# 2. USER QUESTION
# ---------------------------------------------------
question = "What are the company policies on leave?"   # <-- change later

retrieved_docs = retriever.invoke(question)
context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
print(context_text)

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
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
answer = llm.invoke(final_prompt)

# ---------------------------------------------------
# 5. PRINT ANSWER
# ---------------------------------------------------
print("\n========== ANSWER ==========")
print(answer.content)
print("End")
print("============================\n")
