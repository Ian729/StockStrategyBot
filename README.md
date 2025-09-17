# Stock Strategy Bot

一个自动化的每日投资建议生成器，基于财经新闻（RSS）与市场数据（CSV）分析，为指定的标的给出当日操作建议。

## 功能
- 自动收集财经新闻（RSS）并保存为 JSON
- 下载并解析市场数据 CSV（Nikkei 225 / Nasdaq / S&P 500 / Gold）
- 将新闻与市场趋势一并送入模型，生成每日操作建议
- 支持 Nasdaq、日经225、标普500、黄金价格
- 建议类型：定投、卖出、持有观望（定投金额 ≤ 1000）

## 目录结构

```
stock-strategy-bot/
├── .github/
│   └── workflows/
│       └── daily-analysis.yml
├── data/
│   ├── rss_sources.json
│   ├── news.json
│   └── market.json
├── reports/
│   └── YYYY-MM-DD.md
├── src/
│   ├── fetch_news.py
│   ├── fetch_markets.py
│   └── analyze.py
├── README.md
├── requirements.txt
└── LICENSE
```

## 快速开始

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 配置环境变量（GitHub Models 密钥）

```bash
# Windows PowerShell 示例
$env:MODELS_API_KEY="<your_token>"

# macOS/Linux 示例
export MODELS_API_KEY="<your_token>"
```

3. 拉取新闻与市场数据并生成报告（本地）

```bash
python src/fetch_news.py
python src/fetch_markets.py
python src/analyze.py
```

4. 查看每日报告

`reports/YYYY-MM-DD.md`

## 数据来源
- RSS 新闻源配置：`data/rss_sources.json`
- 市场数据（CSV）：
  - Nikkei 225: https://www.forecasts.org/inf/nik225-data.csv
  - Nasdaq: https://www.forecasts.org/inf/nasdaq-data.csv
  - S&P 500: https://www.forecasts.org/inf/sp-500-data.csv
  - Gold: https://www.forecasts.org/inf/gold-data.csv

## 自动化（GitHub Actions）

本项目通过 GitHub Actions 每日自动运行：
- 步骤：安装依赖 → 拉取新闻 → 拉取市场数据 → 调用模型分析 → 生成并提交报告
- 工作流文件：`.github/workflows/daily-analysis.yml`

```yaml
name: Daily Stock Strategy Analysis
on:
  schedule:
    - cron: '0 1 * * *'
  workflow_dispatch:
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python src/fetch_news.py
      - run: python src/fetch_markets.py
      - run: python src/analyze.py
        env:
          MODELS_API_KEY: ${{ secrets.MODELS_API_KEY }}
```

备注：请在仓库的 `Secrets and variables > Actions` 中添加 `MODELS_API_KEY`。
