# Enterprise DocuMind — Multimodal RAG Intelligence Platform

An enterprise-grade, multimodal Retrieval-Augmented Generation (RAG) platform engineered for layout-aware document ingestion, fast vector retrieval, and citation-grounded synthesis.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![PyTest Coverage](https://img.shields.io/badge/pytest-100%25%20coverage-brightgreen?logo=pytest&logoColor=white)](https://docs.pytest.org)
[![Live API](https://img.shields.io/badge/Render-Live%20API-46E3B7?logo=render&logoColor=white)](https://enterprise-documind.onrender.com/docs)

---

## 🚀 Live System Links
- **Interactive Swagger UI Docs:** [https://enterprise-documind.onrender.com/docs](https://enterprise-documind.onrender.com/docs)
- **Health Check Endpoint:** [https://enterprise-documind.onrender.com/health](https://enterprise-documind.onrender.com/health)

---

## 🌟 Key Architecture & Highlights
- **Layout-Aware PDF Ingestion:** Extracts structured tabular data and text chunks while preserving semantic document context.
- **Dynamic Chunking & Dense Embeddings:** Breaks documents into configurable, context-aware chunk windows indexed for fast vector similarity search.
- **Citation-Grounded Synthesis:** Implements algorithmic source scoring to provide exact chunk citations and mitigate hallucinations.
- **Asynchronous FastAPI Microservice:** Designed with async I/O endpoints, strict Pydantic payload models, and CORS middleware.
- **100% Automated Test Coverage:** Thoroughly verified with `pytest` covering API contracts, payload schema edge cases, and retrieval similarity logic.

---

## 🛠️ Tech Stack
- **Backend:** Python 3.11, FastAPI, Pydantic, Uvicorn
- **AI / Retrieval:** Vector Search, Cosine Similarity, Embeddings, Context Chunking
- **Testing & Quality:** PyTest, HTTPX (Async TestClient)
- **Frontend:** React.js, Tailwind CSS
- **Deployment:** Render Cloud, Git / GitHub CI

---

## 📂 Repository Structure

```text
enterprise-documind/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers & endpoints (/upload, /query, /health)
│   │   ├── core/         # Settings, configuration, and app lifespan
│   │   ├── models/       # Pydantic schemas and request/response models
│   │   └── services/     # Ingestion pipelines, vector indexing & RAG engine
│   ├── tests/            # PyTest integration and unit test suite
│   ├── requirements.txt  # Python runtime dependencies
│   └── main.py           # Application entrypoint
├── frontend/             # React dashboard & UI application
└── README.md

Quickstart (Local Development)
1. Backend Setup
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000

API docs will run locally at http://127.0.0.1:8000/docs.

2. Run Test Suite
pytest -v --cov=app

3. Frontend Setup
# Navigate to frontend directory
cd frontend

# Install packages & run
npm install
npm run dev

Core API Specification

Method	Endpoint	Description
GET	/health	Live service health status & uptime check
POST	/api/v1/upload	Multipart file upload, extraction & vector indexing
POST	/api/v1/query	Grounded semantic question answering with citations

👤 Author
Deepa J

LinkedIn: https://www.linkedin.com/in/deepa-j-38a6bb390

GitHub: @dp7639



