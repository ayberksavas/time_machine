"""Pull issues/PRs/events/comments via `gh api`. Events give us the *timeline*, so issue
state can be reconstructed at any T (closed/reopened/labeled/duplicate...)."""
import json
import subprocess
from datetime import datetime
from .store import connect


def ts(s):
    return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()) if s else None


def gh_pages(endpoint, limit=None):
    p = subprocess.run(["gh", "api", "--paginate", "--slurp", endpoint],
                       capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    items = [x for page in json.loads(p.stdout) for x in page]
    return items[:limit] if limit else items


def login(u):
    return (u or {}).get("login")


def ingest_github(slug: str, db_path: str, since: str | None = None):
    db = connect(db_path)
    q = "?state=all&per_page=100&sort=created&direction=asc" + (f"&since={since}" if since else "")
    for i in gh_pages(f"repos/{slug}/issues{q}"):
        db.execute("INSERT OR REPLACE INTO issues VALUES(?,?,?,?,?,?)",
                   (i["number"], int("pull_request" in i), ts(i["created_at"]),
                    login(i["user"]), i["title"], i.get("body") or ""))
        # synthetic 'opened' event with the labels it had at creation is unknown -> use events
    db.execute("DELETE FROM issue_events")
    for e in gh_pages(f"repos/{slug}/issues/events?per_page=100"):
        iss = e.get("issue") or {}
        if not iss:
            continue
        data = {"commit_id": e.get("commit_id"), "label": (e.get("label") or {}).get("name"),
                "rename": e.get("rename"), "dup_of": None}
        db.execute("INSERT INTO issue_events VALUES(?,?,?,?,?)",
                   (iss["number"], ts(e["created_at"]), e["event"], login(e.get("actor")), json.dumps(data)))
    db.execute("DELETE FROM comments")
    for c in gh_pages(f"repos/{slug}/issues/comments?per_page=100"):
        num = int(c["issue_url"].rsplit("/", 1)[-1])
        db.execute("INSERT OR REPLACE INTO comments VALUES(?,?,?,?,?,?)",
                   (c["id"], num, ts(c["created_at"]), login(c["user"]), c["body"], "issue"))
    for c in gh_pages(f"repos/{slug}/pulls/comments?per_page=100"):
        num = int(c["pull_request_url"].rsplit("/", 1)[-1])
        db.execute("INSERT OR REPLACE INTO comments VALUES(?,?,?,?,?,?)",
                   (c["id"], num, ts(c["created_at"]), login(c["user"]), c["body"], "review"))
    db.commit()
