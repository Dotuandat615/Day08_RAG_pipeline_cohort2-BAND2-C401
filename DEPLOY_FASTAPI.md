# Deploy FastAPI đầy đủ

Cloudflare Pages chỉ chạy frontend và Worker JavaScript. Để chạy pipeline RAG đầy đủ trong `api.py`, cần deploy backend Python riêng rồi cấu hình Pages proxy tới backend đó.

## 1. Deploy backend trên Render

1. Push branch `demo` lên GitHub.
2. Vào Render, tạo **New Web Service** từ repo này.
3. Chọn branch `demo`.
4. Chọn Docker deploy. Repo đã có `Dockerfile` và `render.yaml`.
5. Cấu hình environment variables:

```text
OPENAI_API_KEY=<key của bạn>
OPENAI_BASE_URL=https://ckey.vn/v1
OPENAI_MODEL=gpt-5.4-mini
PAGEINDEX_API_KEY=<optional>
```

6. Sau khi deploy xong, kiểm tra:

```text
https://<render-service>.onrender.com/api/health
```

## 2. Nối Cloudflare Pages với backend FastAPI

Trong Cloudflare Pages project `druglaw-rag`, thêm environment variable:

```text
API_BASE_URL=https://<render-service>.onrender.com
```

Sau đó deploy lại Pages:

```bash
npx wrangler pages deploy frontend/ --project-name druglaw-rag --branch main --commit-dirty=true
```

Khi `API_BASE_URL` tồn tại, `frontend/_worker.js` sẽ proxy toàn bộ `/api/*` sang FastAPI backend. Nếu backend lỗi hoặc chưa cấu hình, Worker vẫn dùng câu trả lời fallback để trang không bị chết.

## 3. Local check

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
python -m http.server 3000 --directory frontend
```

Frontend local: `http://127.0.0.1:3000/`

Backend local: `http://127.0.0.1:8000/api/health`
