from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DAILY_DIR = ROOT / "daily"
CSS_VERSION = "20260613-2"


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def cn(value: str) -> str:
    return value


TEXT = {
    "brand": "\u65b0\u80fd\u6e90\u7b80\u62a5",
    "latest": "\u6700\u65b0",
    "archive": "\u5f52\u6863",
    "sources": "\u6765\u6e90",
    "today_focus": "\u4eca\u5929\u5148\u770b\u8fd9 6 \u4e2a\u65b9\u5411",
    "today_focus_copy": "\u4ece\u4ea7\u4e1a\u94fe\u4ef7\u683c\u3001\u9879\u76ee\u62db\u6807\u3001\u50a8\u80fd\u8c03\u5cf0\u5230\u5e76\u7f51\u6d88\u7eb3\uff0c\u628a\u65b0\u80fd\u6e90\u65e5\u62a5\u62c6\u6210\u4f60\u65e9\u4e0a\u771f\u80fd\u5438\u6536\u7684\u5224\u65ad\u7ebf\u3002",
    "sections": "\u4e2a\u65b9\u5411",
    "signals": "\u4e2a\u4ef7\u683c\u4fe1\u53f7",
    "concept": "\u6bcf\u65e5\u6982\u5ff5",
    "capabilities": [
        ("\u5149\u4f0f", "\u5149\u4f0f\u4e0d\u53ea\u770b\u88c5\u673a", "\u628a\u7845\u6599\u3001\u7ec4\u4ef6\u3001\u5206\u5e03\u5f0f\u548c\u7535\u7ad9\u6295\u8d44\u6536\u76ca\u653e\u5230\u4e00\u8d77\u770b\u3002"),
        ("\u98ce\u7535", "\u98ce\u7535\u770b\u8282\u70b9", "\u62db\u6807\u3001\u4e2d\u6807\u4ef7\u3001\u5e76\u7f51\u65f6\u95f4\u662f\u5224\u65ad\u533a\u57df\u70ed\u5ea6\u7684\u524d\u7f6e\u4fe1\u53f7\u3002"),
        ("\u50a8\u80fd", "\u50a8\u80fd\u770b\u6536\u76ca\u673a\u5236", "\u8c03\u5cf0\u8865\u507f\u3001\u5bb9\u91cf\u8865\u507f\u548c\u8f85\u52a9\u670d\u52a1\u51b3\u5b9a\u5546\u4e1a\u6a21\u5f0f\u3002"),
        ("\u7535\u7f51", "\u9879\u76ee\u8981\u843d\u5730", "\u9001\u51fa\u5de5\u7a0b\u3001\u5347\u538b\u7ad9\u548c\u6d88\u7eb3\u8fb9\u754c\u5f80\u5f80\u51b3\u5b9a\u6295\u8fd0\u8282\u594f\u3002"),
        ("\u4ea4\u6613", "\u7535\u4ef7\u8981\u62c6\u5f00\u770b", "\u673a\u5236\u7535\u4ef7\u3001\u7eff\u7535\u6ea2\u4ef7\u3001\u7eff\u8bc1\u548c\u73b0\u8d27\u4ef7\u5dee\u4e0d\u6df7\u5728\u4e00\u8d77\u3002"),
        ("\u653f\u7b56", "\u6587\u4ef6\u8981\u8bfb\u5230\u9879\u76ee\u91cc", "\u628a\u5b98\u65b9\u653f\u7b56\u7ffb\u8bd1\u6210\u5f00\u53d1\u8fb9\u754c\u3001\u5e76\u7f51\u8282\u594f\u548c\u6536\u76ca\u53e3\u5f84\u3002"),
    ],
    "details": "\u4eca\u65e5\u8be6\u60c5",
    "why": "\u4e3a\u4ec0\u4e48\u91cd\u8981\uff1a",
    "read_source": "\u67e5\u770b\u539f\u6587",
    "price_watch": "\u4ef7\u683c\u89c2\u5bdf",
    "price_trend": "\u4ef7\u683c\u8d8b\u52bf",
    "learn_one": "\u4eca\u5929\u53ea\u5b66\u4e00\u4e2a\u6982\u5ff5",
    "source_links": "\u539f\u6587\u548c\u5b66\u4e60\u5165\u53e3",
    "history": "\u5386\u53f2\u5f52\u6863",
}


def load_issues() -> list[dict]:
    issues: list[dict] = []
    for path in sorted(DATA_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            issues.append(json.load(handle))
    return sorted(issues, key=lambda item: item.get("date", ""), reverse=True)


def safe_hero_line(value: str) -> str:
    parts = str(value or "").split("<br>")
    return "<br>".join(esc(part) for part in parts)


def page_shell(title: str, body: str, prefix: str = "") -> str:
    brand = TEXT["brand"]
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{prefix}assets/styles.css?v={CSS_VERSION}">
</head>
<body>
  <nav class="site-nav">
    <div class="nav-inner">
      <a class="nav-brand" href="{prefix}index.html">{esc(brand)}</a>
      <div class="nav-links">
        <a href="{prefix}index.html">{esc(TEXT["latest"])}</a>
        <a href="{prefix}archive.html">{esc(TEXT["archive"])}</a>
        <a href="#sources">{esc(TEXT["sources"])}</a>
      </div>
    </div>
  </nav>

  {body}
</body>
</html>
"""


def render_preview_rows(sections: list[dict]) -> str:
    rows = []
    for index, section in enumerate(sections, start=1):
        section_id = esc(section.get("id", f"section-{index}"))
        rows.append(
            f'<a class="pill-row" href="#{section_id}">'
            f'<span>{index:02d}</span><strong>{esc(section.get("title"))}</strong></a>'
        )
    return "\n".join(rows)


def render_capabilities() -> str:
    cards = []
    for label, title, copy in TEXT["capabilities"]:
        cards.append(
            f"""
        <article class="feature">
          <small>{esc(label)}</small>
          <h3>{esc(title)}</h3>
          <p>{esc(copy)}</p>
        </article>"""
        )
    return "\n".join(cards)


def render_section_cards(sections: list[dict], issue_date: str) -> str:
    cards = []
    for index, section in enumerate(sections, start=1):
        tags = "".join(f"<span>{esc(tag)}</span>" for tag in section.get("tags", []))
        cards.append(
            f"""
        <article id="{esc(section.get("id", f"section-{index}"))}" class="section-card">
          <div class="rank">{index:02d}</div>
          <div>
            <p class="section-label">{esc(section.get("label"))} / {esc(issue_date)}</p>
            <h2>{esc(section.get("title"))}</h2>
            <p>{esc(section.get("summary"))}</p>
            <div class="why"><strong>{esc(TEXT["why"])}</strong>{esc(section.get("why_it_matters"))}</div>
            <div class="tags">{tags}</div>
            <a class="source-action" href="{esc(section.get("url"))}" target="_blank" rel="noreferrer">{esc(TEXT["read_source"])}</a>
          </div>
        </article>"""
        )
    return "\n".join(cards)


def render_price_rows(price_watch: list[dict]) -> str:
    rows = []
    for item in price_watch:
        value = max(0, min(100, int(item.get("value", 0))))
        rows.append(
            f"""
        <div class="price-row">
          <div class="price-head"><span>{esc(item.get("label"))}</span><strong>{esc(item.get("level"))}</strong></div>
          <div class="track"><i style="--w:{value}%"></i></div>
        </div>"""
        )
    return "\n".join(rows)


def build_tariff_trend(issues: list[dict]) -> list[dict]:
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
                        "note": tariff.get("note", "")
                    })
                    break
        trend.append({
            "id": item_id,
            "label": latest_item.get("label", ""),
            "unit": latest_item.get("unit", ""),
            "latest_level": latest_item.get("level", ""),
            "latest_value": float(latest_item.get("value", 0)),
            "note": latest_item.get("note", ""),
            "points": points
        })
    return trend


def format_price(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def price_line_geometry(points: list[dict], width: int = 520, height: int = 180) -> tuple[str, str, str]:
    if not points:
        return "", "", ""
    values = [float(point["value"]) for point in points]
    minimum = min(values)
    maximum = max(values)
    padding = max((maximum - minimum) * 0.2, 0.006)
    low = minimum - padding
    high = maximum + padding
    if high == low:
        high += 0.01
        low -= 0.01

    coords = []
    circles = []
    for index, point in enumerate(points):
        x = 0 if len(points) == 1 else index / (len(points) - 1) * width
        ratio = (float(point["value"]) - low) / (high - low)
        y = height - ratio * height
        coords.append(f"{x:.1f},{y:.1f}")
        circles.append(f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="6" />')

    area = " ".join([f"0,{height}", *coords, f"{width},{height}"])
    return " ".join(coords), area, "".join(circles)


def render_price_trend_page(issues: list[dict]) -> str:
    trend = build_tariff_trend(issues)
    latest = issues[0]
    cards = []
    for item in trend:
        points = item["points"]
        first = points[0]["value"] if points else item["latest_value"]
        latest_value = item["latest_value"]
        delta = latest_value - first
        delta_text = f"+{delta:.3f}" if delta > 0 else f"{delta:.3f}"
        direction = "上行" if delta > 0 else ("下行" if delta < 0 else "持平")
        line_points, area_points, dot_points = price_line_geometry(points)
        date_labels = "".join(f"<span>{esc(point['date'][5:])}</span>" for point in points)
        point_labels = "".join(
            f"<li><span>{esc(point['date'][5:])}</span><strong>{esc(format_price(point['value']))}</strong></li>"
            for point in points
        )
        cards.append(f"""
      <article class="tariff-card">
        <div class="tariff-head">
          <div>
            <p class="section-label">今日电价</p>
            <h2>{esc(item["label"])}</h2>
          </div>
          <div class="tariff-price"><b>{esc(format_price(latest_value))}</b><span>{esc(item["unit"])}</span></div>
        </div>
        <div class="tariff-meta"><span>{esc(item["latest_level"])}</span><span>较首日 {esc(delta_text)}，{esc(direction)}</span></div>
        <svg class="tariff-chart" viewBox="0 0 520 220" role="img" aria-label="{esc(item["label"])}趋势图">
          <line class="grid" x1="0" y1="40" x2="520" y2="40" />
          <line class="grid" x1="0" y1="110" x2="520" y2="110" />
          <line class="grid strong" x1="0" y1="180" x2="520" y2="180" />
          <polygon class="area" points="{area_points}" />
          <polyline class="line" points="{line_points}" />
          {dot_points}
        </svg>
        <div class="trend-dates">{date_labels}</div>
        <ul class="tariff-points">{point_labels}</ul>
        <p class="trend-note">{esc(item.get("note") or "该电价为每日简报维护的新能源交易参考值，后续自动化每天更新。")}</p>
      </article>""")

    body = f"""
  <main class="trend-page">
    <section class="trend-hero">
      <p class="eyebrow">{esc(TEXT["brand"])} / {esc(latest.get("date"))}</p>
      <h1>新能源电价趋势</h1>
      <p>每天固定记录光伏、风电今日参考电价，观察上网与交易价格的连续变化。</p>
    </section>
    <section class="tariff-grid">
{''.join(cards)}
    </section>
  </main>
"""
    return page_shell(f'{TEXT["brand"]} - 新能源电价趋势', body, "")


def render_sources(source_links: list[dict]) -> str:
    links = []
    for source in source_links:
        links.append(
            f"""
        <a href="{esc(source.get("url"))}" target="_blank" rel="noreferrer">
          {esc(source.get("title"))}
          <span>{esc(source.get("source"))}</span>
        </a>"""
        )
    return "\n".join(links)


def render_daily(issue: dict, prefix: str = "") -> str:
    issue_date = issue.get("date", "")
    sections = issue.get("sections", [])
    price_watch = issue.get("price_watch", [])
    learning = issue.get("learning_card", {})
    body = f"""
  <main>
    <section class="hero">
      <div>
        <p class="eyebrow">{esc(TEXT["brand"])} / {esc(issue.get("weekday"))} {esc(issue.get("generated_at"))}</p>
        <h1 class="hero-title">{safe_hero_line(issue.get("hero_line_zh") or issue.get("headline"))}</h1>
        <p class="hero-copy">{esc(issue.get("daily_judgment"))}</p>

        <div class="device">
          <div class="device-screen">
            <div class="screen-main">
              <h2>{esc(TEXT["today_focus"])}</h2>
              <p>{esc(TEXT["today_focus_copy"])}</p>
              <div class="screen-list">{render_preview_rows(sections)}</div>
            </div>
            <div class="screen-side">
              <div class="mini"><b>{len(sections)}</b><span>{esc(TEXT["sections"])}</span></div>
              <div class="mini"><b>{len(price_watch)}</b><span>{esc(TEXT["signals"])}</span></div>
              <div class="mini"><b>{esc(learning.get("term"))}</b><span>{esc(TEXT["concept"])}</span></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="capabilities">
{render_capabilities()}
    </section>

    <section class="section-grid">
      <div class="detail-card">
        <p class="section-label">{esc(TEXT["details"])} / {esc(issue_date)}</p>
{render_section_cards(sections, issue_date)}
      </div>
      <aside class="side-stack">
        <a class="price-card price-link-card" href="{prefix}price.html">
          <p class="section-label">{esc(TEXT["price_watch"])}</p>
{render_price_rows(price_watch)}
          <span class="price-more">\u67e5\u770b\u8d8b\u52bf\u56fe</span>
        </a>
        <section class="learning-card">
          <p class="section-label">{esc(TEXT["learn_one"])}</p>
          <h3>{esc(learning.get("term"))}</h3>
          <p>{esc(learning.get("plain_explanation"))}</p>
          <p>{esc(learning.get("project_angle"))}</p>
        </section>
      </aside>
    </section>

    <section id="sources" class="sources">
      <div class="source-list">
        <p class="section-label">{esc(TEXT["source_links"])}</p>
{render_sources(issue.get("source_links", []))}
      </div>
    </section>
  </main>
"""
    return page_shell(f'{TEXT["brand"]} - {issue_date}', body, prefix)


def render_archive(issues: list[dict]) -> str:
    rows = []
    for issue in issues:
        rows.append(
            f'<a href="daily/{esc(issue.get("date"))}.html">'
            f'<strong>{esc(issue.get("date"))}</strong><span>{esc(issue.get("headline"))}</span></a>'
        )
    body = f"""
  <main class="archive">
    <h1>{esc(TEXT["history"])}</h1>
    <div class="archive-list">{"".join(rows)}</div>
  </main>
"""
    return page_shell(f'{TEXT["brand"]}{TEXT["history"]}', body, "")


def main() -> None:
    DAILY_DIR.mkdir(exist_ok=True)
    issues = load_issues()
    if not issues:
        raise SystemExit("No issue data found.")

    latest = issues[0]
    (ROOT / "index.html").write_text(render_daily(latest, ""), encoding="utf-8")
    for issue in issues:
        (DAILY_DIR / f"{issue.get('date')}.html").write_text(render_daily(issue, "../"), encoding="utf-8")
    (ROOT / "archive.html").write_text(render_archive(issues), encoding="utf-8")
    (ROOT / "price.html").write_text(render_price_trend_page(issues), encoding="utf-8")


if __name__ == "__main__":
    main()
