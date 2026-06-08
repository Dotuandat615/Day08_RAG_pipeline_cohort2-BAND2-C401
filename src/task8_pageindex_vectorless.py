"""
Task 8 — PageIndex Vectorless RAG.

Đăng ký tài khoản tại: https://pageindex.ai/
SDK & sample code: https://github.com/VectifyAI/PageIndex

PageIndex cho phép RAG mà không cần vector store — sử dụng
structural understanding của document thay vì embedding.

Cài đặt:
    pip install pageindex

Hướng dẫn:
    1. Đăng ký account tại pageindex.ai
    2. Lấy API key
    3. Upload documents
    4. Query sử dụng PageIndex API
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def _extract_documents(list_response):
    """PageIndex SDK returns a dict with documents; keep this tolerant for SDK changes."""
    if isinstance(list_response, dict):
        return list_response.get("documents", [])
    if isinstance(list_response, list):
        return list_response
    return []


def upload_documents():
    """
    Upload toàn bộ markdown documents lên PageIndex.
    """
    if not PAGEINDEX_API_KEY or PAGEINDEX_API_KEY == "pi_xxx":
        print("⚠ PAGEINDEX_API_KEY is not configured or invalid.")
        return

    from pageindex import PageIndexClient
    client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

    try:
        docs_resp = client.list_documents()
        existing_names = {d["name"] for d in _extract_documents(docs_resp)}
    except Exception as e:
        print(f"Error listing documents: {e}")
        existing_names = set()

    # Scan for PDF files in the data directory (PageIndex only supports PDF)
    pdf_files = list(STANDARDIZED_DIR.parent.glob("**/*.pdf"))
    
    for pdf_file in pdf_files:
        if not pdf_file.is_file():
            continue
        
        # Avoid duplicate uploads by name comparison
        if pdf_file.name in existing_names:
            print(f"  - Document {ascii(pdf_file.name)} already exists. Skipping upload.")
            continue

        print(f"Uploading {ascii(pdf_file.name)}...")
        try:
            resp = client.submit_document(file_path=str(pdf_file))
            print(f"  [OK] Uploaded: {ascii(pdf_file.name)}, ID: {resp.get('doc_id')}")
        except Exception as e:
            print(f"  [FAIL] Failed to upload {ascii(pdf_file.name)}: {e}")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless retrieval sử dụng PageIndex.
    Dùng làm fallback khi hybrid search không có kết quả tốt.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict,
            'source': 'pageindex'   # Đánh dấu nguồn retrieval
        }
    """
    if not PAGEINDEX_API_KEY or PAGEINDEX_API_KEY == "pi_xxx":
        print("[WARN] PAGEINDEX_API_KEY is not configured or invalid.")
        return []

    from pageindex import PageIndexClient
    client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

    try:
        # Step 1: List documents
        docs_resp = client.list_documents()
        documents = _extract_documents(docs_resp)
        if not documents:
            print("[WARN] No documents found in PageIndex.")
            return []

        # Step 2: Query each document in parallel
        from concurrent.futures import ThreadPoolExecutor
        import time

        def query_single_doc(doc):
            doc_id = doc["id"]
            doc_name = doc["name"]
            try:
                # Submit query
                sub_resp = client.submit_query(doc_id=doc_id, query=query)
                retrieval_id = sub_resp.get("retrieval_id")
                if not retrieval_id:
                    return []

                # Poll until complete
                while True:
                    ret_resp = client.get_retrieval(retrieval_id)
                    status = ret_resp.get("status")
                    if status == "completed":
                        return (doc_name, ret_resp)
                    elif status == "failed":
                        print(f"  [FAIL] Retrieval failed for doc {ascii(doc_name)}")
                        return []
                    time.sleep(0.5)
            except Exception as ex:
                message = str(ex)
                if "Insufficient credits" in message:
                    print("[ERROR] PageIndex has insufficient credits. Purchase more at https://dash.pageindex.ai/subscription.")
                else:
                    print(f"Error querying doc {ascii(doc_name)}: {ex}")
                return []

        results = []
        with ThreadPoolExecutor(max_workers=min(len(documents), 5)) as executor:
            query_results = executor.map(query_single_doc, documents)

        # Step 3: Process and format candidates
        candidates = []
        for q_res in query_results:
            if not q_res:
                continue
            doc_name, ret_resp = q_res
            # Extract nodes and their relevant contents
            nodes = ret_resp.get("retrieved_nodes", [])
            for node in nodes:
                node_score = node.get("score", 1.0)
                relevant_contents = node.get("relevant_contents", [])
                for content_item in relevant_contents:
                    content_str = content_item.get("relevant_content", "")
                    page_idx = content_item.get("page_index")
                    if content_str:
                        candidates.append({
                            "content": content_str,
                            "score": float(node_score),
                            "metadata": {
                                "source": doc_name,
                                "page": page_idx,
                                "node_id": node.get("node_id")
                            },
                            "source": "pageindex"
                        })

        # Step 4: Sort and return top_k
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:top_k]

    except Exception as e:
        print(f"[ERROR] PageIndex search error: {e}")
        return []


if __name__ == "__main__":
    if not PAGEINDEX_API_KEY or PAGEINDEX_API_KEY == "pi_xxx":
        print("[WARN] Hay set PAGEINDEX_API_KEY trong file .env")
        print("  Dang ky tai: https://pageindex.ai/")
    else:
        print("Uploading documents...")
        upload_documents()

        print("\nTest query:")
        results = pageindex_search("hình phạt sử dụng ma tuý", top_k=3)
        for r in results:
            print(f"[{r['score']:.3f}] {ascii(r['content'][:100])}...")
