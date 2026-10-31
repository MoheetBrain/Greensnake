"""Source-URL liveness checking.

A hallucinated citation almost always fails to resolve, so this is a real
anti-fabrication control as well as link-rot monitoring.

The hard part is telling "this page does not exist" from "this publisher blocks
robots". Reuters, CNBC, Bloomberg, the WSJ, BusinessWire and Forbes all serve
401/403/429 to non-browser clients; those pages are real and a researcher reading
them in a browser saw real content. Treating them as dead would condemn most of
the high-quality secondary evidence in the project.

So: browser-realistic headers, HEAD then GET, and an explicit "server answered,
therefore the URL exists" class. Only a genuine 404/410, or a total failure to
connect, counts as non-resolving -- and those are reported for human triage
rather than silently dropped, because a dead link does not make a claim false,
it makes it uncheckable.
"""
from __future__ import annotations

import concurrent.futures as cf
from datetime import datetime

import requests

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}
TIMEOUT = 30
# The server answered. The URL exists; access is gated, not absent.
ALIVE_EVEN_IF_ERROR = {401, 402, 403, 405, 406, 429, 451, 503, 999}
DEAD = {404, 410}


def _variants(url: str) -> list[str]:
    """The same page under www / non-www.

    Sites that canonicalise to one form return a hard 404 on the other, which
    looks exactly like link rot but is not. Checking both stops a live citation
    being condemned over a hostname prefix.
    """
    out = [url]
    if "://www." in url:
        out.append(url.replace("://www.", "://", 1))
    else:
        out.append(url.replace("://", "://www.", 1))
    return out


def _probe(url: str) -> int | None:
    last = None
    for method in ("head", "get"):
        try:
            r = requests.request(method, url, headers=HEADERS, timeout=TIMEOUT,
                                 allow_redirects=True, stream=(method == "get"))
            code = r.status_code
            if method == "get":
                r.close()
            if code < 400 or code in ALIVE_EVEN_IF_ERROR:
                return code
            last = code
        except requests.RequestException:
            continue
    return last


def check_one(url: str) -> tuple[int | None, str | None]:
    """Return (status, resolving_variant). The cited URL is never rewritten."""
    for i, cand in enumerate(_variants(url)):
        code = _probe(cand)
        if is_resolving(code):
            return code, (None if i == 0 else cand)
        if i == 0:
            first = code
    return first, None


def is_resolving(status: int | None) -> bool:
    if status is None:
        return False
    return status < 400 or status in ALIVE_EVEN_IF_ERROR


def check_all(con, limit: int | None = None, workers: int = 12,
              recheck: bool = False) -> dict:
    where = "" if recheck else "WHERE url_http_status IS NULL"
    rows = list(con.execute(
        f"SELECT DISTINCT url FROM sources {where}"
        + (f" LIMIT {int(limit)}" if limit else "")))
    urls = [r["url"] for r in rows]
    now = datetime.utcnow().isoformat(timespec="seconds")
    results: dict[str, tuple[int | None, str | None]] = {}
    if urls:
        with cf.ThreadPoolExecutor(max_workers=workers) as ex:
            for url, res in zip(urls, ex.map(check_one, urls)):
                results[url] = res
    for url, (status, resolved) in results.items():
        con.execute("UPDATE sources SET url_http_status=?, url_checked_at=?, url_resolved=?"
                    " WHERE url=?", (status, now, resolved, url))
    con.commit()
    ok = [u for u, (s, _) in results.items() if is_resolving(s)]
    via_variant = [u for u, (s, rv) in results.items() if is_resolving(s) and rv]
    dead = sorted(u for u, (s, _) in results.items() if s in DEAD)
    unreachable = sorted(u for u, (s, _) in results.items() if s is None)
    return {"checked": len(results), "resolving": len(ok), "resolved_via_variant": via_variant,
            "failing": len(dead) + len(unreachable),
            "dead_404": dead, "unreachable": unreachable,
            "failing_urls": dead + unreachable}


def load_cache(con, path) -> int:
    """Re-apply a previous liveness sweep after a destructive rebuild.

    Liveness is expensive and the database is rebuilt from scratch every run, so
    results are cached by URL. Cached statuses are real measurements, just
    possibly older -- `url_checked_at` carries the date they were taken.
    """
    import json
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return 0
    data = json.loads(p.read_text())
    n = 0
    for url, vals in data.items():
        status, checked_at = vals[0], vals[1]
        resolved = vals[2] if len(vals) > 2 else None
        cur = con.execute("UPDATE sources SET url_http_status=?, url_checked_at=?,"
                          " url_resolved=? WHERE url=? AND url_checked_at IS NULL",
                          (status, checked_at, resolved, url))
        n += cur.rowcount
    con.commit()
    return n


def save_cache(con, path) -> int:
    import json
    from pathlib import Path
    rows = {u: (s, t, rv) for u, s, t, rv in con.execute(
        "SELECT url, url_http_status, url_checked_at, url_resolved FROM sources"
        " WHERE url_checked_at IS NOT NULL")}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(rows, indent=0, sort_keys=True))
    return len(rows)
