"""
Task 6 — Lexical Search Module (BM25).

Mặc định sử dụng BM25. Nếu dùng phương pháp khác (TF-IDF, Elasticsearch,
Weaviate BM25 built-in), hãy giải thích cơ chế trong buổi demo → +5 bonus.

Cài đặt:
    pip install rank-bm25

BM25 hoạt động thế nào:
    - Term Frequency (TF): từ xuất hiện nhiều trong document → điểm cao
    - Inverse Document Frequency (IDF): từ hiếm → quan trọng hơn
    - Document length normalization: document dài không bị ưu tiên quá mức
    - Formula: score(q,d) = Σ IDF(qi) * (tf(qi,d) * (k1+1)) / (tf(qi,d) + k1*(1-b+b*|d|/avgdl))
    - k1=1.5 (term saturation), b=0.75 (length normalization)
"""

from pathlib import Path
import re
import unicodedata

# TODO: Load corpus từ data/standardized/ hoặc từ vector store
def load_corpus() -> list[dict]:
    store_file = Path(__file__).parent.parent / "data" / "vector_store.json"
    if not store_file.exists():
        return []
    try:
        import json
        return json.loads(store_file.read_text(encoding="utf-8"))
    except Exception:
        return []

CORPUS: list[dict] = load_corpus()
_BM25_INDEX = None


def tokenize(text: str) -> list[str]:
    """Normalize Vietnamese text for BM25 while preserving article numbers."""
    normalized = unicodedata.normalize("NFD", text.lower())
    without_marks = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    return re.findall(r"[a-z0-9]+", without_marks)


def build_bm25_index(corpus: list[dict]):
    """
    Xây dựng BM25 index từ corpus.

    Args:
        corpus: List of {'content': str, 'metadata': dict}
    """
    if not corpus:
        return None
    from rank_bm25 import BM25Okapi
    tokenized_corpus = [tokenize(doc["content"]) for doc in corpus]
    return BM25Okapi(tokenized_corpus)


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm từ khóa sử dụng BM25.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,      # BM25 score
            'metadata': dict
        }
        Sorted by score descending.
    """
    global CORPUS, _BM25_INDEX
    if not CORPUS:
        CORPUS = load_corpus()
    
    if not CORPUS:
        return []

    if _BM25_INDEX is None:
        _BM25_INDEX = build_bm25_index(CORPUS)

    if _BM25_INDEX is None:
        return []

    import numpy as np
    tokenized_query = tokenize(query)
    scores = _BM25_INDEX.get_scores(tokenized_query)

    # Get top_k indices
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "content": CORPUS[idx]["content"],
            "score": float(scores[idx]),
            "metadata": CORPUS[idx]["metadata"]
        })
    return results


if __name__ == "__main__":
    # Test
    results = lexical_search("Điều 248 tàng trữ trái phép chất ma tuý", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {ascii(r['content'][:100])}...")
