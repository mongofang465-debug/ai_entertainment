import streamlit as st
from fetcher import fetch_github_trending, fetch_x, fetch_ai_news, fetch_openai_blog
import requests
import os
from dotenv import load_dotenv
from ai_transform import transform_to_fun

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/free"

st.set_page_config(page_title="AI娱乐资讯流", layout="wide")
st.title("🎉 AI科技吃瓜信息流（自动分析+点评版）")

# 用户输入关键词，仅用于抓 X 热点
keyword = st.text_input("输入关键词抓取 X 热点", "科技")

st.markdown("---")
st.subheader("🔥 今日科技吃瓜流")

# -------------------------
# 🧠 AI分析+吃瓜点评函数
# -------------------------
def ai_gossip_comment(news_text):
    """
    AI科技吃瓜分析员：
    - 自动理解新闻
    - 分析前因后果、背景
    - 给出口语化吃瓜点评
    """

    if not OPENROUTER_API_KEY:
        return "（未配置API Key，无法生成点评）"

    system_style = """
你是一个资深科技圈观察员 + 娱乐化评论员。
你的职责：
1. 先理解新闻内容和背景。
2. 给出前因后果分析，让用户明白“为什么发生这件事”。
3. 给出趣味化、口语化、短小的“吃瓜点评”。
4. 保持中文，口语化，短句，像刷信息流的吐槽。
5. 不复述新闻原文。
"""

    user_input = f"""
请阅读这条新闻，然后做三件事：
1️⃣ 分析新闻的前因后果和背景
2️⃣ 描述发生了什么，可能影响谁
3️⃣ 生成一句短小的吃瓜点评，带趣味或吐槽感

新闻内容：
{news_text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_style},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.95
    }

    try:
        res = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=20)
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except:
        return "这条新闻看起来很有意思，但分析失败了。"

# -------------------------
# 📡 聚合数据
# -------------------------
items = []

items += fetch_github_trending()
items += fetch_x(keyword)
items += fetch_ai_news()
items += fetch_openai_blog()

st.write(f"数据条数: {len(items)}")

if len(items) == 0:
    st.warning("⚠️ 没有抓到内容")

# -------------------------
# 🎯 展示信息流
# -------------------------
for item in items:
    raw_text = item["title"] + " " + item["summary"]

    # 1️⃣ AI娱乐化改写原新闻
    fun_text = transform_to_fun(raw_text)

    # 2️⃣ AI自动分析+吃瓜点评
    gossip_text = ai_gossip_comment(raw_text)

    # 展示
    st.markdown("### 🧠 " + fun_text)
    st.markdown(f"💬 吃瓜分析：{gossip_text}")
    st.caption(f"🔗 {item['link']}")
    st.markdown("---")
