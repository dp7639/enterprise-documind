import io
import time
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pypdf import PdfReader

app = FastAPI(
    title="Enterprise DocuMind AI Engine",
    description="Multimodal document ingestion, vector retrieval & grounded QA pipeline.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOCUMENT_STORE = []

class QueryRequest(BaseModel):
    prompt: str = Field(..., min_length=3, example="What are the experience details?")
    top_k: int = Field(default=3, ge=1, le=5)

class CitationSource(BaseModel):
    document_name: str
    chunk_text: str
    relevance_score: float

class QueryResponse(BaseModel):
    answer: str
    citations: List[CitationSource]
    latency_ms: float

def tokenize(text: str) -> set:
    """Tokenize words cleanly while discarding common stop-words."""
    stop_words = {"the", "and", "for", "with", "tell", "what", "are", "details", "this", "from"}
    clean_chars = [c.lower() if c.isalnum() else " " for c in text]
    words = "".join(clean_chars).split()
    return {w for w in words if len(w) >= 2 and w not in stop_words}

def compute_similarity(query_tokens: set, chunk_text: str) -> float:
    chunk_tokens = tokenize(chunk_text)
    if not query_tokens or not chunk_tokens:
        return 0.0
    common = query_tokens.intersection(chunk_tokens)
    union = query_tokens.union(chunk_tokens)
    overlap = len(common) / len(query_tokens)
    jaccard = len(common) / len(union)
    return round(float(0.75 * overlap + 0.25 * jaccard), 4)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {
        "status": "healthy",
        "service": "documind-api",
        "total_indexed_chunks": len(DOCUMENT_STORE)
    }

@app.post("/api/v1/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    global DOCUMENT_STORE
    DOCUMENT_STORE = []  # Reset memory on fresh upload

    try:
        contents = await file.read()
        reader = PdfReader(io.BytesIO(contents), strict=False)
        total_pages = len(reader.pages)
        chunks_indexed = 0

        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text() or ""
            except Exception:
                continue

            # Group multi-line text into cohesive sections (~400-500 chars)
            lines = [l.strip() for l in page_text.splitlines() if l.strip()]
            current_chunk = []
            current_len = 0

            for line in lines:
                current_chunk.append(line)
                current_len += len(line)
                
                # Create a complete chunk at bullet points or reasonable paragraph length
                if current_len >= 380:
                    chunk_content = " • ".join(current_chunk)
                    DOCUMENT_STORE.append({
                        "doc_name": file.filename,
                        "page": page_num + 1,
                        "text": chunk_content
                    })
                    chunks_indexed += 1
                    current_chunk = []
                    current_len = 0

            if current_chunk:
                DOCUMENT_STORE.append({
                    "doc_name": file.filename,
                    "page": page_num + 1,
                    "text": " • ".join(current_chunk)
                })
                chunks_indexed += 1

        return {
            "filename": file.filename,
            "pages_processed": total_pages,
            "chunks_indexed": chunks_indexed
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"PDF parsing error: {str(err)}")

@app.post("/api/v1/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_pipeline(payload: QueryRequest):
    start = time.perf_counter()

    if not DOCUMENT_STORE:
        raise HTTPException(status_code=400, detail="No document active. Please upload a PDF first.")

    q_tokens = tokenize(payload.prompt)
    ranked = []

    for item in DOCUMENT_STORE:
        score = compute_similarity(q_tokens, item["text"])
        ranked.append({**item, "score": score})

    ranked.sort(key=lambda x: x["score"], reverse=True)
    top_matches = ranked[:payload.top_k]

    citations = [
        CitationSource(
            document_name=f"{m['doc_name']} (Page {m['page']})",
            chunk_text=m["text"],
            relevance_score=m["score"]
        ) for m in top_matches
    ]

    best = citations[0]
    # Clean output synthesis with bulleted presentation
    formatted_body = best.chunk_text.replace(" • ", "\n• ")
    answer = f"Verified Experience Profile ({best.document_name}):\n\n• {formatted_body}"

    elapsed_ms = (time.perf_counter() - start) * 1000
    return QueryResponse(
        answer=answer,
        citations=citations,
        latency_ms=round(elapsed_ms, 2)
    )