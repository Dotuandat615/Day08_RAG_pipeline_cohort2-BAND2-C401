"""
RAG Chatbot FastAPI Backend
Deploy: uvicorn api:app --host 0.0.0.0 --port 8000
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

app = FastAPI(
    title="DrugLaw RAG Chatbot API",
    description="RAG pipeline cho pháp luật ma tuý và tin tức liên quan",
    version="1.0.0"
)

# CORS cho Cloudflare Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cập nhật domain Cloudflare Pages sau khi deploy
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
frontend_path = Path(__file__).parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


# =============================================================================
# Request / Response Models
# =============================================================================

class ChatRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5
    use_reranking: Optional[bool] = True
    conversation_history: Optional[list] = []

class SourceChunk(BaseModel):
    content: str
    score: float
    source: str
    metadata: dict

class ChatResponse(BaseModel):
    answer: str
    sources: list
    retrieval_source: str
    latency_ms: int
    num_chunks: int


# =============================================================================
# RAG Pipeline (lazy load để tránh slow startup)
# =============================================================================

_pipeline_ready = False

def ensure_pipeline():
    global _pipeline_ready
    if not _pipeline_ready:
        vector_store = Path(__file__).parent / "data" / "vector_store.json"
        if not vector_store.exists():
            try:
                from src.task4_chunking_indexing import run_pipeline
                run_pipeline()
            except Exception as e:
                print(f"[WARN] Pipeline init failed: {e}")
        _pipeline_ready = True


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/")
async def root():
    """Serve frontend HTML."""
    index_path = Path(__file__).parent / "frontend" / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "DrugLaw RAG API is running. Frontend not found."}


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "pipeline": "hybrid-search + cross-encoder-rerank + pageindex-fallback"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint. Runs full RAG pipeline and returns answer with citations.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    start_time = time.time()

    try:
        ensure_pipeline()

        # Build context-aware question if there's conversation history
        question = request.question
        if request.conversation_history:
            # Simple context injection from last 2 turns
            recent = request.conversation_history[-2:]
            history_text = "\n".join([
                f"User: {turn['user']}\nAssistant: {turn['assistant'][:200]}..."
                for turn in recent
            ])
            question = f"[Lịch sử hội thoại gần đây:\n{history_text}]\n\nCâu hỏi hiện tại: {request.question}"

        from src.task10_generation import generate_with_citation
        result = generate_with_citation(question, top_k=request.top_k)

        latency_ms = int((time.time() - start_time) * 1000)

        # Format sources for frontend
        formatted_sources = []
        for i, chunk in enumerate(result.get("sources", []), 1):
            meta = chunk.get("metadata", {})
            formatted_sources.append({
                "index": i,
                "content": chunk.get("content", "")[:500],  # Truncate for response
                "full_content": chunk.get("content", ""),
                "score": round(float(chunk.get("score", 0)), 4),
                "source": meta.get("source", f"Source {i}"),
                "type": meta.get("type", "unknown"),
                "chunk_id": meta.get("chunk_id", ""),
                "retrieval_method": chunk.get("source", "hybrid"),
            })

        return ChatResponse(
            answer=result.get("answer", "Không thể tạo câu trả lời"),
            sources=formatted_sources,
            retrieval_source=result.get("retrieval_source", "hybrid"),
            latency_ms=latency_ms,
            num_chunks=len(formatted_sources)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {str(e)}")


@app.post("/api/retrieve")
async def retrieve_only(request: ChatRequest):
    """
    Retrieve only — trả về danh sách chunks mà không generate answer.
    Hữu ích cho debug và evaluation.
    """
    try:
        ensure_pipeline()
        from src.task9_retrieval_pipeline import retrieve
        chunks = retrieve(
            request.question,
            top_k=request.top_k,
            use_reranking=request.use_reranking
        )
        return {"chunks": chunks, "count": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config")
async def get_config():
    """Returns current pipeline configuration."""
    return {
        "embedding_model": "BAAI/bge-m3",
        "reranker": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "llm_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "llm_base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "retrieval": {
            "strategy": "hybrid (BM25 + Dense) + RRF fusion",
            "reranking": "Cross-Encoder",
            "fallback": "PageIndex Vectorless RAG",
            "score_threshold": 0.3,
            "default_top_k": 5
        },
        "generation": {
            "temperature": 0.3,
            "top_p": 0.9,
            "reordering": "Lost-in-the-Middle prevention [1,3,5,...,4,2]",
            "citation_format": "[Source Name, Article/Year]"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
