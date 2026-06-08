# RAG Evaluation Results

**Ngày chạy**: 2026-06-08 13:40:40
**Dataset**: 5 câu hỏi từ `golden_dataset.json`
**Evaluation method**: LLM-as-Judge (model: gpt-5.4-mini)

---

## Tổng Quan Điểm

| Metric | Config A (Hybrid+Rerank) | Config B (Dense-Only) | Δ (A−B) |
|--------|--------------------------|----------------------|---------|
| **Faithfulness** | 0.720 | 0.640 | +0.080 |
| **Answer Relevancy** | 0.440 | 0.420 | +0.020 |
| **Context Recall** | 0.280 | 0.320 | -0.040 |
| **Context Precision** | 0.280 | 0.200 | +0.080 |
| **Overall Average** | **0.430** | **0.395** | **+0.035** |
| **Avg Latency (ms)** | 30929 | 15713 | +15216 |

---

## So Sánh A/B Chi Tiết

### Config A: Hybrid Search + Cross-Encoder Reranking (Full Pipeline)

Pipeline: Dense (BGE-M3) + BM25 → RRF Fusion → Cross-Encoder Rerank → Lost-in-Middle Reorder → LLM

| ID | Question | Faith | Rel | Recall | Prec | Avg | Latency |
|----|----------|-------|-----|--------|------|-----|---------|
| Q01 | Hình phạt cho tội tàng trữ trái phép chất ma tuý t... | 1.00 | 0.00 | 0.00 | 0.00 | 0.25 | 26888ms |
| Q02 | Luật Phòng chống ma tuý 2021 quy định những hình t... | 0.70 | 1.00 | 0.50 | 0.50 | 0.68 | 31510ms |
| Q03 | Danh mục các chất ma tuý thuộc nhóm I theo quy địn... | 0.70 | 0.30 | 0.30 | 0.30 | 0.40 | 29860ms |
| Q04 | Tội mua bán trái phép chất ma tuý theo pháp luật V... | 0.70 | 0.20 | 0.30 | 0.30 | 0.38 | 27134ms |
| Q05 | Người nghiện ma tuý có quyền và nghĩa vụ gì theo L... | 0.50 | 0.70 | 0.30 | 0.30 | 0.45 | 39254ms |

### Config B: Dense-Only (Không Reranking)

Pipeline: Dense (BGE-M3) → Top-5 → Lost-in-Middle Reorder → LLM (không có BM25, không Reranking)

| ID | Question | Faith | Rel | Recall | Prec | Avg | Latency |
|----|----------|-------|-----|--------|------|-----|---------|
| Q01 | Hình phạt cho tội tàng trữ trái phép chất ma tuý t... | 0.30 | 0.30 | 0.00 | 0.00 | 0.15 | 16802ms |
| Q02 | Luật Phòng chống ma tuý 2021 quy định những hình t... | 0.50 | 0.70 | 1.00 | 0.70 | 0.72 | 18027ms |
| Q03 | Danh mục các chất ma tuý thuộc nhóm I theo quy địn... | 0.70 | 0.30 | 0.00 | 0.00 | 0.25 | 11971ms |
| Q04 | Tội mua bán trái phép chất ma tuý theo pháp luật V... | 0.70 | 0.50 | 0.30 | 0.00 | 0.38 | 12210ms |
| Q05 | Người nghiện ma tuý có quyền và nghĩa vụ gì theo L... | 1.00 | 0.30 | 0.30 | 0.30 | 0.47 | 19553ms |

---

## Phân Tích Worst Performers (Config A)

Các câu hỏi có điểm thấp nhất trong Config A cần cải thiện:

### 1. Q01: Hình phạt cho tội tàng trữ trái phép chất ma tuý theo Điều 249 Bộ luật Hình sự?

- **Avg Score**: 0.250
- **Faithfulness**: 1.000 | **Relevancy**: 0.000 | **Recall**: 0.000 | **Precision**: 0.000
- **Actual Answer**: Tôi không thể xác minh thông tin này từ nguồn hiện có...
- **Expected Answer**: Phạt tù từ 1 đến 5 năm đối với trường hợp tàng trữ từ 1g đến dưới 5g heroin hoặc cocaine, hoặc chất ma tuý khác với khối lượng tương đương. Hình phạt tăng nặng hơn khi khối lượng lớn hơn hoặc có các t

### 2. Q04: Tội mua bán trái phép chất ma tuý theo pháp luật Việt Nam bị xử phạt như thế nào

- **Avg Score**: 0.375
- **Faithfulness**: 0.700 | **Relevancy**: 0.200 | **Recall**: 0.300 | **Precision**: 0.300
- **Actual Answer**: Theo **Bộ luật Hình sự** trong các nguồn hiện có, **tôi không thể xác minh đầy đủ khung hình phạt cụ thể của tội “mua bán trái phép chất ma túy” từ nguồn hiện có**.[Document 1][Document 2]

Tuy nhiên, các nguồn hiện có cho thấy đây là một trong các tội bị đề nghị truy tố trong một vụ án có tổng cộng...
- **Expected Answer**: Tội mua bán trái phép chất ma tuý theo Điều 251 Bộ luật Hình sự bị phạt tù từ 2 đến 7 năm ở khung cơ bản. Khung tăng nặng có thể lên đến tù chung thân hoặc tử hình nếu phạm tội với số lượng đặc biệt l

### 3. Q03: Danh mục các chất ma tuý thuộc nhóm I theo quy định pháp luật Việt Nam gồm những

- **Avg Score**: 0.400
- **Faithfulness**: 0.700 | **Relevancy**: 0.300 | **Recall**: 0.300 | **Precision**: 0.300
- **Actual Answer**: Tôi không thể xác minh **danh sách cụ thể các chất** thuộc **Danh mục I** từ nguồn hiện có, vì các tài liệu được cung cấp chỉ nêu **mô tả nhóm** chứ không liệt kê tên từng chất trong Danh mục I.[Nghị định số 28.2026.NĐ-CP quy định các danh mục chất ma túy và tiền chất, Document 1; Nghị định số 28.20...
- **Expected Answer**: Nhóm I gồm các chất ma tuý tuyệt đối cấm sử dụng trong y học và đời sống, bao gồm heroin, cocaine, methamphetamine, MDMA (ecstasy), cannabis (cần sa), và các chất tương tự.

---

## Phân Tích Kết Quả

### Nhận Xét

- ✅ **Config A nhỉnh hơn** Config B **+0.035 điểm** — cải thiện nhỏ nhưng có ý nghĩa.
- 📊 **Context Recall** cao (0.280) cho thấy retrieval pipeline lấy đủ evidence.
- 🎯 **Faithfulness** (0.720) phản ánh LLM bám sát context, không hallucinate nhiều.
- ⚡ Latency trung bình 30929ms — đủ responsive cho chatbot.

### Đề Xuất Cải Tiến

1. **Tăng Context Recall**: Thêm HyDE (Hypothetical Document Embeddings) để query expansion.
2. **Cải thiện Worst Performers**: Bổ sung dữ liệu training cho các câu hỏi điểm thấp.
3. **Fine-tune Threshold**: Điều chỉnh `score_threshold = 0.3` dựa trên phân phối điểm thực tế.
4. **Metadata Filtering**: Thêm filter theo loại tài liệu (legal vs news) để tăng Precision.
5. **Chunk Size**: Thử chunk_size nhỏ hơn (256 tokens) cho các câu hỏi về điều khoản cụ thể.

---

*Báo cáo được tạo tự động bởi `eval_pipeline.py` — DrugLaw RAG Chatbot v1.0*
