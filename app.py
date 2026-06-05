# app.py
import streamlit as st
from fetcher import fetch_github_trending, fetch_x, fetch_ai_news, fetch_openai_blog
from ai_transform import transform_to_fun

st.set_page_config(page_title="AI娱乐资讯流", layout="wide")
st.title("🎉 AI娱乐资讯信息流（动态keyword+吃瓜版）")

# 用户前端输入的关键词
keyword = st.text_input("输入关键词", "科技")

st.markdown("---")
st.subheader("🔥 今日科技吃瓜流")

# 聚合数据
items = []
items += fetch_github_trending()
items += fetch_x(keyword)
items += fetch_ai_news()
items += fetch_openai_blog()

# debug 输出
st.write(f"数据条数: {len(items)}")
if len(items) == 0:
    st.warning("⚠️ 没有抓到内容，请检查网络或RSS源。")

# 展示信息流
for item in items:
    raw_text = item["title"] + " " + item["summary"]
    
    # 1️⃣ AI 娱乐化原文
    fun_text = transform_to_fun(raw_text)
    
    # 2️⃣ AI 生成一句“吃瓜点评”，基于前端 keyword
    gossip_prompt = f"""
你是科技娱乐编辑。根据这条科技新闻生成一句简短的“吃瓜点评”：
- 口语化、幽默、带吐槽感
- 20~30字
- 中文
- 关键词：{keyword}
内容：
{raw_text}
"""
    gossip_text = transform_to_fun(gossip_prompt)

    # 展示
    st.markdown("### 🧠 " + fun_text)
    st.markdown(f"💬 吃瓜点评：{gossip_text}")
    st.caption(f"🔗 {item['link']}")
    st.markdown("---")
