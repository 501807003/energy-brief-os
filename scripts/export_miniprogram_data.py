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
    latest_tariffs = chronological[-1].get("tariff_watch", []) if chronological else []
    trend = []

    for latest_item in latest_tariffs:
        item_id = latest_item.get("id")
        points = []
        for issue in chronological:
            for tariff in issue.get("tariff_watch", []):
                if tariff.get("id") == item_id:
                    points.append({
                        "date": issue.get("date", ""),
                        "value": float(tariff.get("value", 0)),
                        "level": tariff.get("level", ""),
                        "note": tariff.get("note", ""),
                    })
                    break

        trend.append({
            "id": item_id,
            "label": latest_item.get("label", ""),
            "unit": latest_item.get("unit", ""),
            "latestLevel": latest_item.get("level", ""),
            "latestValue": float(latest_item.get("value", 0)),
            "note": latest_item.get("note", ""),
            "points": points,
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
