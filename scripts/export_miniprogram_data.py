from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MINIPROGRAM_DATA = ROOT / "wechat-miniprogram" / "utils" / "issues.js"


def load_issues() -> list[dict]:
    issues: list[dict] = []
    for path in sorted(DATA_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            issues.append(json.load(handle))
    return sorted(issues, key=lambda issue: issue.get("date", ""), reverse=True)


def build_price_trend(issues: list[dict]) -> list[dict]:
    chronological = sorted(issues, key=lambda issue: issue.get("date", ""))
    latest_watch = chronological[-1].get("price_watch", []) if chronological else []
    series_count = min(4, len(latest_watch))
    trend = []

    for index in range(series_count):
        latest_item = latest_watch[index]
        points = []
        for issue in chronological:
            watch = issue.get("price_watch", [])
            if index >= len(watch):
                continue
            item = watch[index]
            points.append({
                "date": issue.get("date", ""),
                "value": max(0, min(100, int(item.get("value", 0)))),
                "level": item.get("level", "")
            })
        trend.append({
            "label": latest_item.get("label", ""),
            "latestLevel": latest_item.get("level", ""),
            "latestValue": max(0, min(100, int(latest_item.get("value", 0)))),
            "points": points
        })

    return trend


def main() -> None:
    issues = load_issues()
    if not issues:
        raise SystemExit("No issue data found.")

    payload = {
        "latestDate": issues[0]["date"],
        "issues": {issue["date"]: issue for issue in issues},
        "priceTrend": build_price_trend(issues),
        "archive": [
            {
                "date": issue["date"],
                "weekday": issue.get("weekday", ""),
                "headline": issue.get("headline", ""),
            }
            for issue in issues
        ],
    }

    MINIPROGRAM_DATA.parent.mkdir(parents=True, exist_ok=True)
    content = "const briefData = "
    content += json.dumps(payload, ensure_ascii=False, indent=2)
    content += ";\n\nmodule.exports = briefData;\n"
    MINIPROGRAM_DATA.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
