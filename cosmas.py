
from datetime import datetime, timezone
import html
import requests

KEYWORDS = ["python", "automation", "scraper", "ai", "writing", "coordinator"]

def check_remotive_jobs():
    url = "https://remotive.com/api/remote-jobs?limit=30"
    resp = requests.get(url, timeout=15).json()
    matches = []
    for job in resp.get("jobs", []):
        title = job.get("title", "")
        if any(k in title.lower() for k in KEYWORDS):
            matches.append({
                "title": title,
                "company": job.get("company_name", "Unknown"),
                "category": job.get("category", ""),
                "url": job.get("url", "#"),
            })
    return matches[:15]

def build_html(jobs):
    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    cards = ""
    for job in jobs:
        cards += f"""
        <div class="card">
            <h3><a href="{html.escape(job['url'])}" target="_blank" rel="noopener">{html.escape(job['title'])}</a></h3>
            <p class="meta">{html.escape(job['company'])} &bull; {html.escape(job['category'])}</p>
        </div>
        """

    if not cards:
        cards = "<p>No matching opportunities found on this check. Check back soon.</p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cosmas Opportunity Board</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; background: #f8fafc; color: #0f172a; }}
        header {{ margin-bottom: 1.5rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 1rem; }}
        h1 {{ margin: 0 0 0.25rem 0; color: #1e3a8a; }}
        .timestamp {{ color: #64748b; font-size: 0.9rem; }}
        .card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 0.9rem; }}
        .card h3 {{ margin: 0 0 0.35rem 0; font-size: 1.05rem; }}
        .card a {{ color: #2563eb; text-decoration: none; }}
        .card a:hover {{ text-decoration: underline; }}
        .meta {{ margin: 0; color: #475569; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <header>
        <h1>Cosmas Opportunity Board</h1>
        <p class="timestamp">Last updated: {updated_at} &bull; Auto-refreshes every 15 minutes</p>
    </header>
    <main>
        {cards}
    </main>
</body>
</html>
"""

def main():
    jobs = check_remotive_jobs()
    page = build_html(jobs)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Generated index.html with {len(jobs)} matching jobs.")

if __name__ == "__main__":
    main()

