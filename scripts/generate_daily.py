from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DAILY_DIR = ROOT / "daily"


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def page_shell(title: str, body: str, prefix: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{prefix}assets/styles.css">
</head>
<body>
  <nav class="site-nav">
    <div class="nav-inner">
      <a class="nav-brand" href="{prefix}index.html">新能源简报</a>
      <div class="nav-links">
        <a href="{prefix}index.html">最新</a>
        <a href="{prefix}archive.html">归档</a>
        <a href="#sources">来源</a>
      </div>
    </div>
  </nav>
  {body}
</body>
</html>
"""


def render_tags(tags: list[str]) -> str:
    return "".join(f"<span>{esc(tag)}</span>" for tag in tags)


def render_daily(issue: dict, prefix: str = "") -> str:
    date = esc(issue["date"])
    top_items = issue.get("top_items", [])[:3]
    price_watch = issue.get("price_watch", [])
    learning = issue.get("learning_card", {})
    source_links = issue.get("source_links", [])
    hero_copy = issue.get("daily_judgment")
    hero_copy_html = f'<p class="hero-copy">{esc(hero_copy)}</p>' if hero_copy else ""

    preview_rows = "".join(
        f'<div class="pill-row">{idx:02d} {esc(item.get("title"))}</div>'
        for idx, item in enumerate(top_items, start=1)
    )
    mini_cards = f"""
      <div class="mini"><b>{len(top_items)}</b><span>今日重点</span></div>
      <div class="mini"><b>{len(issue.get('policy_items', [])) or 3}</b><span>政策信号</span></div>
      <div class="mini"><b>{len(price_watch)}</b><span>价格信号</span></div>
    """

    capability_cards = "".join(
        f"""
        <article class="feature">
          <small>{label}</small>
          <h3>{headline}</h3>
          <p>{copy}</p>
        </article>
        """
        for label, headline, copy in [
            ("政策", "政策只看变化", "从发文中找出对项目判断有用的条款。"),
            ("交易", "交易规则转成人话", "把中长期、现货、绿电与绿证分开讲。"),
            ("电价", "电价有跟踪口径", "机制电价、现货价差、绿证价格不混在一起。"),
            ("学习", "每天一个概念", "用项目经营视角解释一个政策或交易术语。"),
        ]
    )

    news_items = "".join(
        f"""
        <article class="news-item">
          <div class="rank">{idx:02d}</div>
          <div>
            <h2>{esc(item.get('title'))}</h2>
            <p>{esc(item.get('summary'))}</p>
            <div class="why"><strong>为什么重要：</strong>{esc(item.get('why_it_matters') or item.get('why_it_maters'))}</div>
            <div class="tags">{render_tags(item.get('tags', []))}</div>
          </div>
        </article>
        """
        for idx, item in enumerate(top_items, start=1)
    )

    price_rows = "".join(
        f"""
        <div class="price-row">
          <div class="price-head"><span>{esc(row.get('label'))}</span><strong>{esc(row.get('level'))}</strong></div>
          <div class="track"><i style="--w:{int(row.get('value', 0))}%"></i></div>
        </div>
        """
        for row in price_watch
    )

    sources = "".join(
        f"""
        <a href="{esc(link.get('url'))}" target="_blank" rel="noreferrer">
          {esc(link.get('title'))}
          <span>{esc(link.get('source'))}</span>
        </a>
        """
        for link in source_links
    )

    body = f"""
  <main>
    <section class="hero">
      <div>
        <p class="eyebrow">新能源简报</p>
        <h1 class="hero-title">{issue.get('hero_line_zh')}</h1>
        {hero_copy_html}
        <div class="device">
          <div class="device-screen">
            <div class="screen-main">
          <h2>今天最值得看的 3 条信息</h2>
              <p>每条信息都压缩成：发生了什么、为什么重要、接下来该看哪个数字或规则。</p>
              <div class="screen-list">{preview_rows}</div>
            </div>
            <div class="screen-side">{mini_cards}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="capabilities">{capability_cards}</section>

    <section class="section-grid">
      <div class="detail-card">
        <p class="section-label">今日详情 / {date}</p>
        {news_items}
      </div>
      <aside class="side-stack">
        <section class="price-card">
          <p class="section-label">价格观察</p>
          {price_rows}
        </section>
        <section class="learning-card">
          <p class="section-label">今天只学一个概念</p>
          <h3>{esc(learning.get('term'))}</h3>
          <p>{esc(learning.get('plain_explanation'))}</p>
          <p>{esc(learning.get('project_angle'))}</p>
        </section>
      </aside>
    </section>

    <section id="sources" class="sources">
      <div class="source-list">
        <p class="section-label">原文来源</p>
        {sources}
      </div>
    </section>
  </main>
"""
    return page_shell(f"新能源简报 - {date}", body, prefix=prefix)


def render_archive(issues: list[dict]) -> str:
    rows = "".join(
        f'<a href="daily/{esc(issue["date"])}.html"><strong>{esc(issue["date"])}</strong><span>{esc(issue.get("daily_judgment") or issue.get("headline"))}</span></a>'
        for issue in issues
    )
    body = f"""
  <main class="archive">
    <h1>历史归档</h1>
    <div class="archive-list">{rows}</div>
  </main>
"""
    return page_shell("新能源简报历史归档", body)


def load_issues() -> list[dict]:
    issues = []
    for path in sorted(DATA_DIR.glob("*.json")):
        issues.append(json.loads(path.read_text(encoding="utf-8")))
    return sorted(issues, key=lambda item: item["date"], reverse=True)


def main() -> None:
    DAILY_DIR.mkdir(exist_ok=True)
    issues = load_issues()
    if not issues:
        raise SystemExit("No data files found in data/")

    for issue in issues:
        (DAILY_DIR / f"{issue['date']}.html").write_text(render_daily(issue, prefix="../"), encoding="utf-8")

    latest = issues[0]
    (ROOT / "index.html").write_text(render_daily(latest), encoding="utf-8")
    (ROOT / "archive.html").write_text(render_archive(issues), encoding="utf-8")


if __name__ == "__main__":
    main()
