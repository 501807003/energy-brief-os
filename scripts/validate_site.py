from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DAILY_DIR = ROOT / "daily"

REQUIRED_SECTION_IDS = {"solar", "wind", "storage", "grid", "market", "policy"}
BAD_TEXT_MARKERS = ["\ufffd", "\u93c2", "\u59e3", "\u951b", "\u9286"]
OLD_ENGLISH_COPY = "Track three lines first today"
HERO_TITLE = "\u6bcf\u5929\u65e9\u4e0a<br>\u8bfb\u61c2\u65b0\u80fd\u6e90"
GENERIC_HOME_URLS = {
    "https://www.nea.gov.cn/",
    "https://www.ndrc.gov.cn/",
    "https://www.gov.cn/",
}


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION FAILED: {message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def latest_issue() -> dict:
    data_files = sorted(DATA_DIR.glob("*.json"))
    if not data_files:
        fail("no issue JSON files found")

    issues = []
    for path in data_files:
        with path.open("r", encoding="utf-8") as handle:
            issues.append(json.load(handle))
    return sorted(issues, key=lambda issue: issue.get("date", ""), reverse=True)[0]


def validate_issue(issue: dict) -> None:
    issue_date = issue.get("date")
    if not issue_date:
        fail("latest issue has no date")

    sections = issue.get("sections", [])
    section_ids = {section.get("id") for section in sections}
    if section_ids != REQUIRED_SECTION_IDS:
        fail(f"section ids must be {sorted(REQUIRED_SECTION_IDS)}, got {sorted(section_ids)}")

    if len(issue.get("price_watch", [])) < 4:
        fail("price_watch must contain at least 4 items")

    if not issue.get("source_links"):
        fail("source_links must not be empty")

    for section in sections:
        if not section.get("url"):
            fail(f"section {section.get('id')} has no source url")
        if section.get("url") in GENERIC_HOME_URLS:
            fail(f"section {section.get('id')} must link to a concrete article, not a homepage")
        for key in ["title", "summary", "why_it_matters", "label"]:
            if not section.get(key):
                fail(f"section {section.get('id')} missing {key}")


def validate_html(issue: dict) -> None:
    issue_date = issue["date"]
    html_paths = [
        ROOT / "index.html",
        DAILY_DIR / f"{issue_date}.html",
        ROOT / "archive.html",
    ]

    for path in html_paths:
        content = read_text(path)
        for marker in BAD_TEXT_MARKERS:
            if marker in content:
                fail(f"possible mojibake marker found in {path.relative_to(ROOT)}: {marker}")
        if OLD_ENGLISH_COPY in content:
            fail(f"old English copy found in {path.relative_to(ROOT)}")
        if "styles.css?v=" not in content:
            fail(f"stylesheet cache version missing in {path.relative_to(ROOT)}")

    index_html = read_text(ROOT / "index.html")
    daily_html = read_text(DAILY_DIR / f"{issue_date}.html")
    archive_html = read_text(ROOT / "archive.html")

    if f'<h1 class="hero-title">{HERO_TITLE}</h1>' not in index_html:
        fail("hero title split is missing or changed")

    for section_id in REQUIRED_SECTION_IDS:
        if f'href="#{section_id}"' not in index_html:
            fail(f"preview anchor missing: #{section_id}")
        if f'id="{section_id}"' not in index_html:
            fail(f"detail section id missing: {section_id}")

    if index_html.count('class="section-card"') < 6:
        fail("index.html must render at least 6 section cards")
    if daily_html.count('class="source-action"') < 6:
        fail("daily page must render source action buttons")
    if f'daily/{issue_date}.html' not in archive_html:
        fail("archive does not link to latest daily page")


def main() -> None:
    issue = latest_issue()
    validate_issue(issue)
    validate_html(issue)
    print(f"OK: validated daily issue {issue['date']}")


if __name__ == "__main__":
    main()
