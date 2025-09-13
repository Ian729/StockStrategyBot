import json
import requests
from pathlib import Path
from datetime import date


import os
# 配置你的 Github Models API Key，推荐用环境变量 MODELS_API_KEY
MODELS_API_KEY = os.environ.get('MODELS_API_KEY', '')
TARGETS = ['Nasdaq', '日经225', '标普500', '黄金']

PROMPT_TEMPLATE = '''You are an investment advisor. Based on the following news summaries and market trends, generate a daily action suggestion for each target. 
Your output MUST be a valid JSON array, each item must follow this schema:
{{
    "target": "Nasdaq|Nikkei 225|S&P 500|Gold",
    "action": "invest|sell|hold",
    "amount": integer (required if action is invest, 1-1000),
    "reason": string (optional, max 100 chars)
}}
Only three actions are allowed: invest (≤1000), sell, hold. If you are not sure, use hold. Do not output anything except the JSON array.

Example output:
[
    {{"target": "Nasdaq", "action": "invest", "amount": 500, "reason": "positive news"}},
    {{"target": "Nikkei 225", "action": "hold"}},
    {{"target": "S&P 500", "action": "sell", "reason": "negative trend"}},
    {{"target": "Gold", "action": "invest", "amount": 1000}}
]

News summaries:
{news}
'''

def load_news(path='data/news.json'):
    with open(path, 'r', encoding='utf-8') as f:
        news = json.load(f)
    # 只取标题和摘要
    return "\n".join([f"{item['title']} {item['summary']}" for item in news])


def analyze():
    news_text = load_news()
    prompt = PROMPT_TEMPLATE.format(news=news_text)
    # TODO: Replace the following with actual Github Models API endpoint and authentication
    url = "https://models.github.ai/inference/chat/completions"
    headers = {
        "Authorization": f"Bearer {MODELS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4.1",  # Replace with Github Models model name
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        suggestion = response.json()['choices'][0]['message']['content']
    else:
        suggestion = f"[Error] Github Models API call failed: {response.status_code}\n{response.text}"
    today = date.today().isoformat()
    report_path = f"reports/{today}.md"
    Path(report_path).write_text(suggestion, encoding='utf-8')
    print(f"Report saved to {report_path}")

if __name__ == '__main__':
    analyze()
