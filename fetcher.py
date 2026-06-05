# fetcher.py
import feedparser
import requests

def fetch_rss(url, limit=5):
    """抓取 RSS 数据，如果失败返回占位"""
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:limit]:
            items.append({
                "title": entry.get("title", "无标题"),
                "link": entry.get("link", "#"),
                "summary": entry.get("summary", "")
            })
        if not items:
            items = [{"title": "RSS源暂无内容", "link": "#", "summary": ""}]
        return items
    except:
        return [{"title": "RSS抓取失败", "link": "#", "summary": ""}]

def fetch_github_trending():
    """抓 GitHub热门库"""
    try:
        url = "https://api.github.com/search/repositories?q=stars:>10000&sort=stars"
        r = requests.get(url, timeout=10)
        data = r.json().get("items", [])[:5]
        if not data:
            raise Exception("GitHub返回为空")
        return [{"title": f"{i['full_name']}", "link": i["html_url"], "summary": i.get("description","")} for i in data]
    except:
        return [{"title": "GitHub抓取失败", "link": "#", "summary": ""}]

def fetch_x(keyword="科技"):
    """模拟 X / Twitter 热点"""
    return [{
        "title": f"{keyword} 在X热议中🔥",
        "link": "#",
        "summary": f"开发者社区正在讨论 {keyword} 的最新动态"
    }]

def fetch_ai_news():
    return fetch_rss("https://www.artificialintelligence-news.com/feed/")

def fetch_openai_blog():
    return fetch_rss("https://openai.com/blog/rss.xml")
