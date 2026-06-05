# ai_transform.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # 读取 .env

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/free"

def transform_to_fun(text):
    """AI娱乐化改写，如果 API 不可用就返回原文"""
    if not OPENROUTER_API_KEY:
        return text

    prompt = f"""
你是一个“AI科技娱乐新闻编辑”。

把下面内容改写成：
- 像科技八卦
- 有一点娱乐/吐槽感
- 适合信息流阅读
- 不超过120字
- 中文口语化

内容：
{text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }

    try:
        res = requests.post(OPENROUTER_API_URL:=OPENROUTER_URL, headers=headers, json=payload, timeout=15)
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except:
        return text