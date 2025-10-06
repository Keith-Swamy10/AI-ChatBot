⚙️ Phase 1: Skeleton & Project Setup

We’ll start with:

Repository structure

FastAPI setup

Environment config (for secrets)

Basic API route stubs (no AI logic yet)

🎯 Goal: You have a clean, scalable codebase ready to plug features into.
This gives structure and avoids spaghetti code once we add FAISS, LLM, and Google Sheets later.

📚 Phase 2: Knowledge Base (FAISS + Embeddings)

We’ll:

Create a folder for company data (docs, policies, FAQs).

Generate embeddings for each file.

Store & query them in FAISS.

🎯 Goal: You can fetch the most relevant context for any query.

🧠 Phase 3: LLM Integration

We’ll:

Hook in an AI model (OpenAI for MVP).

Write a wrapper so you can later swap in Mistral or self-hosted models.

🎯 Goal: Your bot gives meaningful responses from KB context.

📇 Phase 4: Lead Capture

We’ll:

Add logic to detect contact info (email/phone).

Connect to Google Sheets API for storage.

🎯 Goal: The backend can store & manage leads automatically.

🌐 Phase 5: Deployment Prep

We’ll:

Dockerize the app.

Add .env, logging, rate limits, etc.

Prepare for eventual scaling (Gunicorn + Uvicorn).



🎯 Goal: Fully deployable backend, ready for frontend widget integration.chatbot-backend/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── leads.py
│   │
│   ├── core/
│   │   ├── config.py        # Environment variables, global settings
│   │   ├── logger.py        # Logging setup
│   │
│   ├── services/
│   │   ├── llm_service.py   # For OpenAI/Mistral calls (later)
│   │   ├── kb_service.py    # FAISS + embeddings logic (later)
│   │   ├── leads_service.py # For Sheets/DB integration (later)
│   │
│   └── utils/
│       ├── validators.py    # Email/phone regex checks etc.
│
├── .env                     # API keys, secrets
├── requirements.txt
└── README.md
