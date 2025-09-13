# Stock Strategy Bot

一个自动化的每日投资建议生成器，基于财经新闻和市场行情分析，为指定的标的给出当日操作建议。

## 功能
- 自动收集财经新闻（RSS）
- 分析新闻和市场行情，生成每日操作建议
- 支持 Nasdaq、日经225、标普500、黄金价格
- 建议类型：定投、卖出、持有观望

## 目录结构

```
stock-strategy-bot/
├── .github/
│   └── workflows/
│       └── daily-analysis.yml
├── data/
│   └── rss_sources.json
├── reports/
│   └── YYYY-MM-DD.md
├── src/
│   ├── fetch_news.py
│   ├── analyze.py
│   ├── generate_suggestion.py
│   └── utils.py
├── README.md
├── requirements.txt
└── LICENSE
```

## 快速开始

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 手动运行分析

```bash
python src/analyze.py
```

3. 查看每日报告

`reports/YYYY-MM-DD.md`

## 自动化

本项目通过 GitHub Actions 每日自动运行，生成最新投资建议。
