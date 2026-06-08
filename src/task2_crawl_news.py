"""
Task 2 — Crawl bài báo về nghệ sĩ liên quan tới ma tuý.

Hướng dẫn:
    1. Crawl tối thiểu 5 bài báo từ các trang tin tức Việt Nam.
    2. Sử dụng Crawl4AI hoặc thư viện crawling tương tự.
    3. Lưu output vào data/landing/news/
    4. Mỗi bài lưu 1 file JSON với metadata (url, title, date_crawled, content).

Cài đặt:
    pip install crawl4ai
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"


def setup_directory():
    """Tạo thư mục data/landing/news/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# TODO: Điền danh sách URL bài báo cần crawl
ARTICLE_URLS = [
    "https://vietnamnet.vn/de-nghi-truy-to-ca-si-chi-dan-cung-anh-trai-vi-to-chuc-su-dung-ma-tuy-2434484.html",
    "https://vietnamnet.vn/loat-ca-si-dinh-chat-cam-ma-tuy-pha-huy-nao-bo-ngu-tre-ra-sao-2518285.html",
    "https://vietnamnet.vn/3-nu-nghe-si-viet-tu-huy-danh-tieng-vi-lien-quan-den-ma-tuy-2514737.html",
    "https://vietnamnet.vn/chi-dan-an-tay-truc-phuong-la-nhung-mat-xich-cuoi-trong-duong-day-ma-tuy-2342032.html",
    "https://vietnamnet.vn/vi-sao-chi-dan-an-tay-va-nhieu-sao-viet-lien-quan-ma-tuy-2340658.html",
]


async def crawl_article(url: str) -> dict:
    """
    Crawl một bài báo và trả về dict chứa metadata + content.

    Returns:
        {
            "url": str,
            "title": str,
            "date_crawled": str (ISO format),
            "content_markdown": str
        }
    """
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Run requests.get in an executor to make it async-friendly
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.get(url, headers=headers, timeout=15)
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract title
        title_el = soup.find(class_="content-detail-title")
        if not title_el:
            title_el = soup.find("h1")
        title = title_el.text.strip() if title_el else (soup.title.text.strip() if soup.title else "Unknown")

        # Extract content
        body = soup.find("div", class_="maincontent")
        if not body:
            body = soup.find("div", id="maincontent")
        if not body:
            body = soup.find("div", class_="content-detail-body")

        if body:
            paragraphs = [p.text.strip() for p in body.find_all("p") if p.text.strip()]
        else:
            paragraphs = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]

        content_markdown = "\n\n".join(paragraphs)

        return {
            "url": url,
            "title": title,
            "date_crawled": datetime.now().isoformat(),
            "content_markdown": content_markdown,
        }
    except Exception as e:
        print(f"Standard fetch failed for {url}: {e}. Trying Crawl4AI fallback...")

    try:
        from crawl4ai import AsyncWebCrawler
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return {
                "url": url,
                "title": result.metadata.get("title", "Unknown"),
                "date_crawled": datetime.now().isoformat(),
                "content_markdown": result.markdown,
            }
    except Exception as err:
        print(f"Crawl4AI fetch failed for {url}: {err}")
        raise err


async def crawl_all():
    """Crawl toàn bộ bài báo trong ARTICLE_URLS."""
    setup_directory()

    for i, url in enumerate(ARTICLE_URLS, 1):
        print(f"[{i}/{len(ARTICLE_URLS)}] Crawling: {url}")
        article = await crawl_article(url)

        # Lưu file JSON
        filename = f"article_{i:02d}.json"
        filepath = DATA_DIR / filename
        filepath.write_text(json.dumps(article, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  Saved: {filepath.name}")


if __name__ == "__main__":
    if not ARTICLE_URLS:
        print("Warning: Please fill ARTICLE_URLS before running!")
        print("Suggestion: find articles on VnExpress, Tuoi Tre, Thanh Nien, ...")
    else:
        asyncio.run(crawl_all())
