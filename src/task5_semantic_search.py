"""
Task 5 — Semantic Search Module.

Viết module tìm kiếm ngữ nghĩa (dense retrieval) trên vector store.

Yêu cầu:
    - Input: query string + top_k
    - Output: danh sách chunks có score, sorted descending
    - Phải tương thích với embedding model và vector store ở Task 4
"""
_MODEL = None


def _get_model():
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _MODEL


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa sử dụng vector similarity.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,      # Nội dung chunk
            'score': float,      # Cosine similarity score
            'metadata': dict     # source, doc_type, chunk_index
        }
        Sorted by score descending.
    """
    import json
    import numpy as np
    from pathlib import Path

    store_file = Path(__file__).parent.parent / "data" / "vector_store.json"
    if not store_file.exists():
        print("Vector store not found. Please run task4 first.")
        return []

    # Load chunks
    chunks = json.loads(store_file.read_text(encoding="utf-8"))
    if not chunks:
        return []

    # Load same embedding model once per process.
    model = _get_model()
    query_vector = model.encode(query)

    results = []
    for chunk in chunks:
        chunk_vector = np.array(chunk["embedding"])
        
        # Compute cosine similarity
        dot_val = np.dot(query_vector, chunk_vector)
        norm_q = np.linalg.norm(query_vector)
        norm_c = np.linalg.norm(chunk_vector)
        
        if norm_q > 0 and norm_c > 0:
            score = float(dot_val / (norm_q * norm_c))
        else:
            score = 0.0

        results.append({
            "content": chunk["content"],
            "score": score,
            "metadata": chunk["metadata"]
        })

    # Sort descending by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:top_k]


if __name__ == "__main__":
    # Test
    results = semantic_search("hình phạt cho tội tàng trữ ma tuý", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {ascii(r['content'][:100])}...")
