# DrugLaw RAG Chatbot — Sản Phẩm Nhóm Band 2 C401

> Chatbot AI tra cứu pháp luật về ma tuý và chất cấm tại Việt Nam.
> Trả lời mọi câu hỏi với **citation nguồn rõ ràng** từ văn bản pháp luật và báo chí.

---

## Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────────┐
│                    DrugLaw RAG Architecture                      │
└─────────────────────────────────────────────────────────────────┘

  [User Browser]
       │  HTTP/REST (Fetch API)
       ▼
  ┌──────────────┐          ┌─────────────────────────────────────┐
  │  HTML/CSS/JS │          │         FastAPI Backend              │
  │  (Cloudflare │◄────────►│  /api/chat  /api/health  /api/config│
  │   Pages)     │          └──────────────┬──────────────────────┘
  └──────────────┘                         │
                                           ▼
                              ┌────────────────────────┐
                              │   RAG Pipeline Core     │
                              │                         │
                              │  Query                  │
                              │   ├─→ Semantic Search   │
                              │   │   (BAAI/bge-m3)     │
                              │   ├─→ Lexical (BM25)    │
                              │   │                     │
                              │   ├─→ RRF Fusion        │
                              │   ├─→ Cross-Encoder     │
                              │   │   Reranking         │
                              │   │                     │
                              │   └─→ score < 0.3?      │
                              │         └─→ PageIndex   │
                              │             Vectorless  │
                              │                         │
                              │   ↓                     │
                              │  Lost-in-Middle Reorder │
                              │  Context Formatting     │
                              │  LLM Generation         │
                              │  (gpt-5.4-mini @ckey)  │
                              │                         │
                              │  Answer + Citations     │
                              └────────────────────────┘
```

### Công Nghệ Sử Dụng

| Layer | Technology | Mô tả |
|-------|-----------|-------|
| Frontend | HTML/CSS/JS | Dark mode, citation cards, conversation memory |
| Deployment | Cloudflare Pages | CDN toàn cầu, HTTPS miễn phí |
| API | FastAPI (Python) | REST API wrapping RAG pipeline |
| Embedding | BAAI/bge-m3 | Multilingual embedding, tốt cho tiếng Việt |
| Vector Store | ChromaDB (local) | Lưu trữ và tìm kiếm vector |
| Lexical | BM25 (rank-bm25) | Tìm kiếm từ khoá |
| Fusion | RRF | Reciprocal Rank Fusion |
| Reranking | Cross-Encoder | ms-marco-MiniLM-L-6-v2 |
| Fallback | PageIndex SDK | Vectorless RAG cho PDF |
| LLM | gpt-5.4-mini | Qua endpoint ckey.vn |
| Evaluation | LLM-as-Judge | DeepEval-compatible, 4 metrics |

---

## Tính Năng Chatbot

- ✅ **Citation Display** — Mỗi câu trả lời hiển thị nguồn dưới dạng card đẹp có thể expand
- ✅ **Conversation Memory** — Nhớ lịch sử 4 lượt gần nhất cho follow-up questions
- ✅ **Source Viewer** — Xem nội dung chunk gốc, score relevance, loại tài liệu
- ✅ **Kiến trúc sidebar** — Hiển thị architecture diagram và cấu hình pipeline
- ✅ **Session Stats** — Thống kê realtime: số câu hỏi, latency trung bình, hybrid vs pageindex
- ✅ **Responsive** — Hỗ trợ mobile
- ✅ **Status indicator** — Kiểm tra kết nối backend realtime

---

## Hướng Dẫn Chạy

### Cài Đặt

```bash
# Clone repo
git clone <repo-url>
cd Day08_RAG_pipeline_cohort2-BAND2-C401

# Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Cài dependencies
pip install -r requirements.txt

# Cấu hình environment
cp .env.example .env
# Điền API keys vào .env
```

### Chạy Backend

```bash
# Development
uvicorn api:app --host 0.0.0.0 --port 8000 --reload

# Production
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Chạy Frontend (Local)

```bash
# Mở file HTML trực tiếp (kết nối đến localhost:8000)
start frontend/index.html

# Hoặc serve bằng Python
python -m http.server 3000 --directory frontend
# Mở http://localhost:3000
```

### Deploy Cloudflare Pages

```bash
# 1. Cài Wrangler CLI
npm install -g wrangler

# 2. Login Cloudflare
wrangler login

# 3. Deploy frontend
wrangler pages deploy frontend/ --project-name druglaw-rag

# 4. Cập nhật API_BASE trong frontend/index.html
# Thay '' bằng URL backend thực tế (VD: Railway, Render)
```

---

## Evaluation

```bash
# Chạy evaluation (5 câu nhanh)
python group_project/evaluation/eval_pipeline.py

# Chạy đầy đủ 15 câu (đặt QUICK_EVAL=False trong file)
# Kết quả xuất ra: group_project/evaluation/results.md
```

---

## Phân Công Công Việc

| Thành viên | MSSV | Nhiệm vụ | Trạng thái |
|-----------|------|----------|------------|
| (Nhóm trưởng) | | Task 1,2,3 + Kiến trúc hệ thống | ✅ Done |
| | | Task 4,5,6 + Indexing | ✅ Done |
| | | Task 7,8 + Reranking + PageIndex | ✅ Done |
| | | Task 9,10 + Pipeline + Generation | ✅ Done |
| (Nhóm) | | UI/UX HTML + FastAPI + Evaluation | ✅ Done |

---

## Cấu Trúc Thư Mục

```
.
├── api.py                          ← FastAPI backend
├── frontend/
│   └── index.html                  ← HTML/CSS/JS chatbot UI
├── src/
│   ├── task1_collect_legal_docs.py
│   ├── task2_crawl_news.py
│   ├── task3_convert_markdown.py
│   ├── task4_chunking_indexing.py
│   ├── task5_semantic_search.py
│   ├── task6_lexical_search.py
│   ├── task7_reranking.py
│   ├── task8_pageindex_vectorless.py
│   ├── task9_retrieval_pipeline.py
│   └── task10_generation.py
├── group_project/
│   ├── README.md                   ← (file này)
│   └── evaluation/
│       ├── golden_dataset.json     ← 15 Q&A test cases
│       ├── eval_pipeline.py        ← Evaluation script
│       └── results.md              ← Kết quả evaluation
├── data/
│   ├── landing/legal/              ← PDF pháp luật gốc
│   ├── landing/news/               ← JSON bài báo crawl
│   └── standardized/               ← Markdown đã convert
├── tests/
│   └── test_individual.py          ← 35 unit tests (100% pass)
├── requirements.txt
└── .env
```
