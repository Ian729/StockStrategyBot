import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple
import requests

CSV_SOURCES = {
    "Nikkei 225": "https://www.forecasts.org/inf/nik225-data.csv",
    "Nasdaq": "https://www.forecasts.org/inf/nasdaq-data.csv",
    "S&P 500": "https://www.forecasts.org/inf/sp-500-data.csv",
    "Gold": "https://www.forecasts.org/inf/gold-data.csv",
}


def _download_csv(url: str) -> str:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def _parse_rows(csv_text: str) -> List[Tuple[str, float, str]]:
    rows: List[Tuple[str, float, str]] = []
    reader = csv.reader(csv_text.splitlines())
    for row in reader:
        if len(row) < 3:
            continue
        # Expected: Date , VALUE , Note
        date_str = row[0].strip()
        value_str = row[1].strip().replace(',', '')
        note = row[2].strip()
        # Skip header lines that don't parse to float
        try:
            value = float(value_str)
        except ValueError:
            continue
        rows.append((date_str, value, note))
    return rows


def _latest_actual_and_prev(rows: List[Tuple[str, float, str]]) -> Tuple[Tuple[str, float], Tuple[str, float]]:
    # Keep only Actual notes
    actuals = [(d, v) for d, v, note in rows if note.lower().startswith('actual')]
    # Fallback to all rows if none labeled Actual
    series = actuals if actuals else [(d, v) for d, v, _ in rows]
    if len(series) == 0:
        raise ValueError("No data rows parsed")
    # Rows are chronological in these files; keep as-is
    if len(series) == 1:
        return series[-1], series[-1]
    return series[-1], series[-2]


def _trend(curr: float, prev: float) -> str:
    if curr > prev:
        return "up"
    if curr < prev:
        return "down"
    return "flat"


def fetch_markets() -> Dict[str, Dict[str, str]]:
    result: Dict[str, Dict[str, str]] = {}
    for name, url in CSV_SOURCES.items():
        try:
            csv_text = _download_csv(url)
            rows = _parse_rows(csv_text)
            (d_curr, v_curr), (d_prev, v_prev) = _latest_actual_and_prev(rows)
            t = _trend(v_curr, v_prev)
            result[name] = {
                "date": d_curr,
                "value": v_curr,
                "prev_date": d_prev,
                "prev_value": v_prev,
                "trend": t,
            }
        except Exception as e:
            result[name] = {
                "error": str(e)[:200]
            }
    return result


if __name__ == '__main__':
    data = fetch_markets()
    Path('data/market.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print("Saved market data to data/market.json")
