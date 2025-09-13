# Stock Strategy Bot

一个自动化的每日投资建议生成器，基于财经新闻和市场行情分析，为指定的标的给出当日操作建议。

## 🎯 项目目标

* 自动收集各大财经网站头条新闻（通过 RSS）
* 利用 GitHub Models 分析当日新闻和行情
* 输出每日操作建议（支持 Nasdaq、日经225、标普500、黄金价格）
* 建议类型限制为：`定投X元 (≤1000元)`、`卖出X元`、`持有观望`

## 🏗 项目结构

```
stock-strategy-bot/
├── .github/
│   └── workflows/
│       └── daily-analysis.yml   # GitHub Actions 定时任务
├── data/
│   └── rss_sources.json         # RSS源配置
├── reports/
│   └── 2025-09-13.md            # 每日生成报告
├── src/
│   ├── fetch_news.py            # 拉取新闻
│   ├── analyze.py               # 调用AI分析
│   ├── generate_suggestion.py   # 输出建议
│   └── utils.py
├── README.md
├── requirements.txt
└── LICENSE
```

## ⚙️ 安装与使用

1. 克隆仓库

```bash
git clone https://github.com/yourname/stock-strategy-bot.git
cd stock-strategy-bot
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置 RSS 源和 GitHub Models API Key

* 编辑 `data/rss_sources.json`
* 在 GitHub 仓库设置中添加 `GH_TOKEN` 用于调用 GitHub Models

4. 手动运行一次分析（本地）

```bash
python src/fetch_news.py && python src/analyze.py && python src/generate_suggestion.py
```

## 🔄 自动化运行

本项目包含一个 GitHub Actions workflow (`.github/workflows/daily-analysis.yml`)，每天定时执行：

* 拉取最新新闻
* 调用 GitHub Models 分析
* 生成当日建议，写入 `reports/` 文件夹
* 自动提交结果到仓库

## 📊 输出示例

`reports/2025-09-13.md`

```markdown
# 2025-09-13 操作建议

| 资产        | 建议      | 理由摘要 |
|-------------|-----------|---------|
| Nasdaq      | 定投 500元 | 美科技板块利好，资金回流 |
| NI225       | 持有观望 | 日本CPI上涨，观望 |
| S&P 500     | 定投 300元 | 美联储降息预期强烈 |
| Gold Price  | 卖出 200元 | 风险偏好提升，黄金走弱 |
```

## 📅 GitHub Actions Workflow 示例

`.github/workflows/daily-analysis.yml`

```yaml
name: Daily Stock Analysis

on:
  schedule:
    - cron: "0 1 * * *"  # UTC 时间每天 1:00 运行
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run analysis pipeline
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
        run: |
          python src/fetch_news.py
          python src/analyze.py
          python src/generate_suggestion.py

      - name: Commit results
        run: |
          git config --global user.name 'github-actions'
          git config --global user.email 'actions@github.com'
          git add reports/
          git commit -m "chore: add daily report $(date +'%Y-%m-%d')" || echo "No changes to commit"
          git push
```
# Stock Strategy Bot

一个自动化的每日投资建议生成器，基于财经新闻和市场行情分析，为指定的标的给出当日操作建议。

## 🎯 项目目标

* 自动收集各大财经网站头条新闻（通过 RSS）
* 利用 GitHub Models 分析当日新闻和行情
* 输出每日操作建议（支持 Nasdaq、日经225、标普500、黄金价格）
* 建议类型限制为：`定投X元 (≤1000元)`、`卖出X元`、`持有观望`

## 🏗 项目结构

```
stock-strategy-bot/
├── .github/
│   └── workflows/
│       └── daily-analysis.yml   # GitHub Actions 定时任务
├── data/
│   └── rss_sources.json         # RSS源配置
├── reports/
│   └── 2025-09-13.md            # 每日生成报告
├── src/
│   ├── fetch_news.py            # 拉取新闻
│   ├── analyze.py               # 调用AI分析
│   ├── generate_suggestion.py   # 输出建议
│   └── utils.py
├── README.md
├── requirements.txt
└── LICENSE
```

## ⚙️ 安装与使用

1. 克隆仓库

```bash
git clone https://github.com/yourname/stock-strategy-bot.git
cd stock-strategy-bot
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置 RSS 源和 GitHub Models API Key

* 编辑 `data/rss_sources.json`
* 在 GitHub 仓库设置中添加 `GH_TOKEN` 用于调用 GitHub Models

4. 手动运行一次分析（本地）

```bash
python src/fetch_news.py && python src/analyze.py && python src/generate_suggestion.py
```

## 🔄 自动化运行

本项目包含一个 GitHub Actions workflow (`.github/workflows/daily-analysis.yml`)，每天定时执行：

* 拉取最新新闻
* 调用 GitHub Models 分析
* 生成当日建议，写入 `reports/` 文件夹
* 自动提交结果到仓库

## 📊 输出示例

`reports/2025-09-13.md`

```markdown
# 2025-09-13 操作建议

| 资产        | 建议      | 理由摘要 |
|-------------|-----------|---------|
| Nasdaq      | 定投 500元 | 美科技板块利好，资金回流 |
| NI225       | 持有观望 | 日本CPI上涨，观望 |
| S&P 500     | 定投 300元 | 美联储降息预期强烈 |
| Gold Price  | 卖出 200元 | 风险偏好提升，黄金走弱 |
```

## 📅 GitHub Actions Workflow 示例

`.github/workflows/daily-analysis.yml`

```yaml
name: Daily Stock Analysis

on:
  schedule:
    - cron: "0 1 * * *"  # UTC 时间每天 1:00 运行
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run analysis pipeline
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
        run: |
          python src/fetch_news.py
          python src/analyze.py
          python src/generate_suggestion.py

      - name: Commit results
        run: |
          git config --global user.name 'github-actions'
          git config --global user.email 'actions@github.com'
          git add reports/
          git commit -m "chore: add daily report $(date +'%Y-%m-%d')" || echo "No changes to commit"
          git push
```

## 🧠 示例 analyze.py

`src/analyze.py`

```python
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("GH_TOKEN"))

def load_news():
    with open("data/news.json", "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    news = load_news()
    prompt = f"""
你是一个理性的投资顾问。以下是今天的财经新闻：
{json.dumps(news, ensure_ascii=False, indent=2)}

请为以下资产分别给出操作建议：Nasdaq、NI225、S&P 500、Gold Price。
输出格式严格为JSON，键为资产名，值为对象：{{"action": "定投X元|卖出X元|持有观望", "reason": "一句理由"}}
其中X为整数，且定投上限1000元。
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    with open("data/analysis.json", "w", encoding="utf-8") as f:
        f.write(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```
