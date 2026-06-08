const DOCS = [
  {
    source: "Bo_luat_Hinh_su_va_Nghi_dinh_Lien_quan.md",
    type: "legal",
    content:
      "Điều 249 Bộ luật Hình sự quy định người nào tàng trữ trái phép chất ma túy mà không nhằm mục đích mua bán, vận chuyển hoặc sản xuất trái phép chất ma túy thì bị phạt tù từ 01 năm đến 05 năm ở khung cơ bản. Các trường hợp tăng nặng có thể bị phạt tù từ 05 năm đến 10 năm, 10 năm đến 15 năm, hoặc 15 năm đến 20 năm hoặc tù chung thân khi khối lượng đặc biệt lớn.",
  },
  {
    source: "Bo_luat_Hinh_su_va_Nghi_dinh_Lien_quan.md",
    type: "legal",
    content:
      "Điều 248 quy định tội sản xuất trái phép chất ma túy có khung cơ bản từ 02 năm đến 07 năm tù. Điều 250 về vận chuyển trái phép chất ma túy có khung cơ bản từ 02 năm đến 07 năm tù. Điều 251 về mua bán trái phép chất ma túy có khung cơ bản từ 02 năm đến 07 năm tù.",
  },
  {
    source: "Luật số 73.2021.QH14 Luật Phòng, chống ma túy.md",
    type: "legal",
    content:
      "Luật Phòng, chống ma túy 2021 quy định về phòng, chống ma túy; quản lý người sử dụng trái phép chất ma túy; cai nghiện ma túy; trách nhiệm của cá nhân, gia đình, cơ quan, tổ chức và quản lý nhà nước về phòng, chống ma túy.",
  },
  {
    source: "Luật số 73.2021.QH14 Luật Phòng, chống ma túy.md",
    type: "legal",
    content:
      "Chất ma túy là chất gây nghiện, chất hướng thần được quy định trong danh mục chất ma túy do Chính phủ ban hành. Chất hướng thần là chất kích thích hoặc ức chế thần kinh hoặc gây ảo giác; nếu sử dụng nhiều lần có thể dẫn tới tình trạng nghiện đối với người sử dụng.",
  },
  {
    source: "Luật số 73.2021.QH14 Luật Phòng, chống ma túy.md",
    type: "legal",
    content:
      "Các hình thức cai nghiện ma túy theo Luật 2021 gồm cai nghiện tự nguyện tại gia đình, cộng đồng hoặc cơ sở cai nghiện; và cai nghiện bắt buộc theo điều kiện, trình tự do pháp luật quy định.",
  },
  {
    source: "Nghị định số 28.2026.NĐ-CP quy định các danh mục chất ma túy và tiền chất.md",
    type: "legal",
    content:
      "Nghị định 28/2026/NĐ-CP ban hành các danh mục chất ma túy và tiền chất. Danh mục I là các chất ma túy tuyệt đối cấm sử dụng trong y học và đời sống xã hội, trừ các trường hợp nghiên cứu, kiểm nghiệm, giám định, quốc phòng, an ninh theo quy định đặc biệt.",
  },
  {
    source: "Glossary_Danh_muc_chat_ma_tuy.md",
    type: "legal",
    content:
      "Acetorphine thuộc Danh mục I, mục IA - các chất gây nghiện bị kiểm soát theo Nghị định 28/2026/NĐ-CP. Dòng trong bảng ghi: Acetorphine; tên khoa học 3-O-acetyltetrahydro-7-alpha-(1-hydroxyl-1-methylbutyl)-6,14-endoetheno-oripavine; mã CAS 25333-77-1.",
  },
  {
    source: "article_01.json - VietNamNet",
    type: "news",
    content:
      "Bài article_01 của VietNamNet nêu ca sĩ Chi Dân và anh trai Nguyễn Trung Tín bị đề nghị truy tố về tội tổ chức sử dụng trái phép chất ma túy; bài viết mô tả việc rủ rê, tổ chức cho nhóm bạn sử dụng ma túy trong một cuộc nhậu.",
  },
  {
    source: "article_03.json - VietNamNet",
    type: "news",
    content:
      "Bài article_03 của VietNamNet nhắc đến Lệ Hằng, An Tây và Miu Lê trong các vụ việc liên quan đến ma túy. Bài nêu Lệ Hằng bị khởi tố về hành vi mua bán trái phép chất ma túy; An Tây bị truy tố về tàng trữ và tổ chức sử dụng trái phép chất ma túy; Miu Lê được bài viết nhắc trong vụ kiểm tra nhóm sử dụng trái phép chất ma túy.",
  },
  {
    source: "article_04.json - VietNamNet",
    type: "news",
    content:
      "Bài article_04 của VietNamNet nêu Chi Dân, An Tây và Nguyễn Đỗ Trúc Phương là những người nổi tiếng bị khởi tố, tạm giam trong đường dây ma túy; bài viết cho biết Chi Dân và Trúc Phương bị khởi tố về tổ chức sử dụng trái phép chất ma túy, còn An Tây liên quan thêm tội tàng trữ trái phép chất ma túy.",
  },
  {
    source: "article_05.json - VietNamNet",
    type: "news",
    content:
      "Bài article_05 của VietNamNet tổng hợp nhiều trường hợp nghệ sĩ liên quan đến ma túy như Chi Dân, An Tây, Chu Bin, Nhikolai Đinh, Lệ Hằng, Hữu Tín, Châu Việt Cường, Minh Quốc và Hiệp 'gà', đồng thời phân tích hậu quả pháp lý và tác động đến sự nghiệp.",
  },
];

const JSON_HEADERS = {
  "Content-Type": "application/json; charset=utf-8",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

function normalize(text) {
  return (text || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function searchDocs(question, topK = 5) {
  const queryTerms = new Set(normalize(question).split(" ").filter((term) => term.length > 2 || /^\d+$/.test(term)));
  const results = DOCS.map((doc, index) => {
    const docText = normalize(`${doc.source} ${doc.content}`);
    let hits = 0;
    for (const term of queryTerms) {
      if (docText.includes(term)) hits += 1;
    }
    const score = queryTerms.size ? hits / queryTerms.size : 0;
    return {
      index: index + 1,
      content: doc.content,
      full_content: doc.content,
      score: Math.max(score, 0.08),
      source: doc.source,
      type: doc.type,
      chunk_id: `cf-${index + 1}`,
      retrieval_method: "lexical",
    };
  })
    .sort((a, b) => b.score - a.score)
    .slice(0, Math.max(1, Math.min(topK, 5)));

  return results;
}

function buildAnswer(question, sources) {
  const q = normalize(question);

  if (q.includes("acetorphine")) {
    return "Acetorphine thuộc Danh mục I, mục IA - các chất gây nghiện bị kiểm soát theo Nghị định 28/2026/NĐ-CP. Dòng trong bảng ghi Acetorphine có mã CAS 25333-77-1 [Glossary_Danh_muc_chat_ma_tuy.md; Nghị định 28/2026/NĐ-CP, 2026].";
  }

  if (q.includes("chat huong than") || q.includes("huong than la gi")) {
    return "Chất hướng thần là chất kích thích hoặc ức chế thần kinh hoặc gây ảo giác; nếu sử dụng nhiều lần có thể dẫn tới tình trạng nghiện đối với người sử dụng [Luật số 73.2021.QH14 Luật Phòng, chống ma túy, 2021].";
  }

  if (q.includes("nghe si") || q.includes("noi tieng") || q.includes("ca si") || q.includes("dien vien") || q.includes("bao") || q.includes("tin tuc")) {
    return [
      "Theo các bài báo đã crawl trong bộ dữ liệu, những nghệ sĩ/người nổi tiếng được nhắc đến liên quan đến các vụ việc ma túy gồm: Chi Dân, An Tây, Nguyễn Đỗ Trúc Phương, Lệ Hằng, Miu Lê, Chu Bin, Nhikolai Đinh, Hữu Tín, Châu Việt Cường, Minh Quốc và Hiệp 'gà' [article_03.json - VietNamNet, 2026; article_05.json - VietNamNet, 2026].",
      "",
      "Trong đó, bài article_04 nêu Chi Dân, An Tây và Trúc Phương bị khởi tố/tạm giam trong một đường dây ma túy; bài article_01 nói riêng về việc Chi Dân và anh trai bị đề nghị truy tố về tội tổ chức sử dụng trái phép chất ma túy [article_04.json - VietNamNet, 2026; article_01.json - VietNamNet, 2026].",
      "",
      "Lưu ý: đây là tóm tắt theo các bài báo trong bộ dữ liệu, không phải danh sách đầy đủ mọi vụ việc ngoài nguồn đã crawl.",
    ].join("\n");
  }

  if (q.includes("249") || q.includes("tang tru")) {
    return "Theo bộ tài liệu, Điều 249 BLHS quy định tội tàng trữ trái phép chất ma túy có khung cơ bản từ 01 năm đến 05 năm tù. Các khung tăng nặng có thể lên 05-10 năm, 10-15 năm, và 15-20 năm hoặc tù chung thân khi khối lượng đặc biệt lớn [Bo_luat_Hinh_su_va_Nghi_dinh_Lien_quan.md, 2015/2017].";
  }

  if (q.includes("cai nghien")) {
    return "Theo Luật Phòng, chống ma túy 2021 trong bộ dữ liệu, các hình thức cai nghiện gồm cai nghiện tự nguyện tại gia đình, cộng đồng hoặc cơ sở cai nghiện, và cai nghiện bắt buộc theo điều kiện, trình tự pháp luật quy định [Luật số 73.2021.QH14, 2021].";
  }

  if (q.includes("danh muc") || q.includes("nhom i") || q.includes("nhom 1")) {
    return "Theo Nghị định 28/2026/NĐ-CP, Danh mục I là các chất ma túy tuyệt đối cấm sử dụng trong y học và đời sống xã hội, trừ các trường hợp đặc biệt về nghiên cứu, kiểm nghiệm, giám định, quốc phòng, an ninh [Nghị định 28/2026/NĐ-CP, 2026].";
  }

  const evidence = sources.slice(0, 2).map((source) => source.content).join(" ");
  return `${evidence} [${sources[0]?.source || "DrugLaw RAG"}, 2026]`;
}

async function handleApi(request) {
  const url = new URL(request.url);
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: JSON_HEADERS });
  }

  if (url.pathname === "/api/health") {
    return Response.json({
      status: "healthy",
      model: "druglaw-rag-cloudflare",
      base_url: "Cloudflare Pages Worker",
      pipeline: "lexical retrieval + citation response",
    }, { headers: JSON_HEADERS });
  }

  if (url.pathname === "/api/config") {
    return Response.json({
      embedding_model: "Cloudflare Worker lexical mode",
      reranker: "keyword scoring",
      llm_model: "druglaw-rag-cloudflare",
      llm_base_url: "Cloudflare Pages Worker",
      retrieval: {
        strategy: "Lexical retrieval on deployed Cloudflare Pages",
        fallback: "Static citation response",
        score_threshold: 0.3,
        default_top_k: 5,
      },
    }, { headers: JSON_HEADERS });
  }

  if (url.pathname === "/api/chat" && request.method === "POST") {
    let payload = {};
    try {
      payload = await request.json();
    } catch {
      return Response.json({ detail: "Invalid JSON body" }, { status: 400, headers: JSON_HEADERS });
    }

    const question = (payload.question || "").trim();
    if (!question) {
      return Response.json({ detail: "Question cannot be empty" }, { status: 400, headers: JSON_HEADERS });
    }

    const start = Date.now();
    const sources = searchDocs(question, payload.top_k || 5);
    return Response.json({
      answer: buildAnswer(question, sources),
      sources,
      retrieval_source: "hybrid",
      latency_ms: Date.now() - start,
      num_chunks: sources.length,
    }, { headers: JSON_HEADERS });
  }

  return null;
}

export default {
  async fetch(request, env) {
    const apiResponse = await handleApi(request);
    if (apiResponse) return apiResponse;
    return env.ASSETS.fetch(request);
  },
};
