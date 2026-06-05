# app.py
import streamlit as st
from fetcher import fetch_github_trending, fetch_x, fetch_ai_news, fetch_openai_blog
from ai_transform import transform_to_fun

st.set_page_config(page_title="AI娱乐资讯流", layout="wide")
st.title("🎉 AI娱乐资讯信息流（MVP）")

keyword = st.text_input("输入关键词", "AI")

st.markdown("---")
st.subheader("🔥 今日AI吃瓜流")

# 🔥 聚合数据
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
    fun_text = transform_to_fun(item["title"] + " " + item["summary"])
    st.markdown("### 🧠 " + fun_text)
    st.caption(f"🔗 {item['link']}")
    st.markdown("---")