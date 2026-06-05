import feedparser
import requests

# -------------------------
# 1️⃣ RSS（关键词过滤）
# -------------------------
def fetch_rss(url, keyword="", limit=5):
    """RSS + 关键词过滤"""
    try:
        feed = feedparser.parse(url)
        items = []

        for entry in feed.entries:
            text = (entry.get("title", "") + " " + entry.get("summary", "")).lower()

            # 🔥 关键词过滤（核心）
            if keyword.lower() in text or keyword == "":
                items.append({
                    "title": entry.get("title", "无标题"),
                    "link": entry.get("link", "#"),
                    "summary": entry.get("summary", "")
                })

            if len(items) >= limit:
                break

        if not items:
            return [{"title": f"没有找到与【{keyword}】相关内容", "link": "#", "summary": ""}]

        return items

    except:
        return [{"title": "RSS抓取失败", "link": "#", "summary": ""}]


# -------------------------
# 2️⃣ GitHub（关键词搜索版🔥）
# -------------------------
def fetch_github(keyword="AI"):
    """GitHub真实关键词搜索（不是trending）"""
    try:
        url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars"
        r = requests.get(url, timeout=10)
        data = r.json().get("items", [])[:5]

        return [{
            "title": f"{i['full_name']}",
            "link": i["html_url"],
            "summary": i.get("description", "")
        } for i in data]

    except:
        return [{"title": "GitHub搜索失败", "link": "#", "summary": ""}]


# -------------------------
# 3️⃣ X（关键词模拟增强版）
# -------------------------
def fetch_x(keyword="科技"):
    return [{
        "title": f"X平台关于【{keyword}】的热议🔥",
        "link": "#",
        "summary": f"最近社交媒体上关于 {keyword} 的讨论持续升温，开发者和行业人士观点分化明显。"
    }]


# -------------------------
# 4️⃣ AI新闻RSS（保持）
# -------------------------
def fetch_ai_news(keyword=""):
    return fetch_rss("https://www.artificialintelligence-news.com/feed/", keyword)


# -------------------------
# 5️⃣ OpenAI Blog（关键词过滤）
# -------------------------
def fetch_openai_blog(keyword=""):
    return fetch_rss("https://openai.com/blog/rss.xml", keyword)
