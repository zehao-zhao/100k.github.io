#!/usr/bin/env python3
"""Fetch research papers and news for a query and store results as JSON."""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from typing import Any, Dict, List
from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


def _read_json(url: str, headers: Dict[str, str] | None = None) -> Dict[str, Any]:
    request = Request(url, headers=headers or {})
    with urlopen(request, timeout=20) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def _read_xml(url: str) -> str:
    with urlopen(url, timeout=20) as response:  # noqa: S310
        return response.read().decode("utf-8")


def fetch_arxiv(query: str, limit: int) -> List[Dict[str, Any]]:
    url = (
        "http://export.arxiv.org/api/query?search_query=all:"
        f"{quote(query)}&start=0&max_results={limit}"
    )
    feed_xml = _read_xml(url)
    root = ET.fromstring(feed_xml)
    entries = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.findtext("{http://www.w3.org/2005/Atom}title", default="").strip()
        summary = entry.findtext("{http://www.w3.org/2005/Atom}summary", default="").strip()
        published = entry.findtext("{http://www.w3.org/2005/Atom}published", default="")
        link_el = entry.find("{http://www.w3.org/2005/Atom}link")
        link = link_el.attrib.get("href") if link_el is not None else ""
        entries.append(
            {
                "source": "arxiv",
                "title": title,
                "summary": summary,
                "url": link,
                "published": published,
            }
        )
    return entries


def fetch_gdelt(query: str, limit: int) -> List[Dict[str, Any]]:
    url = (
        "https://api.gdeltproject.org/api/v2/doc/doc?query="
        f"{quote(query)}&format=json&maxrecords={limit}&mode=artlist"
    )
    payload = _read_json(url)
    entries = []
    for article in payload.get("articles", []):
        entries.append(
            {
                "source": "news",
                "title": article.get("title", ""),
                "summary": article.get("seendate", ""),
                "url": article.get("url", ""),
                "published": article.get("seendate", ""),
            }
        )
    return entries


def fetch_github(query: str, limit: int, token: str | None) -> List[Dict[str, Any]]:
    url = (
        "https://api.github.com/search/repositories?q="
        f"{quote(query)}&sort=updated&order=desc&per_page={limit}"
    )
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    payload = _read_json(url, headers=headers)
    entries = []
    for repo in payload.get("items", []):
        entries.append(
            {
                "source": "github",
                "title": repo.get("full_name", ""),
                "summary": repo.get("description") or "",
                "url": repo.get("html_url", ""),
                "published": repo.get("updated_at", ""),
            }
        )
    return entries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Results per source")
    parser.add_argument(
        "--sources",
        default="arxiv,news,github",
        help="Comma-separated sources: arxiv, news, github",
    )
    parser.add_argument("--output", default="research_results.json", help="Output JSON file")
    parser.add_argument("--github-token", default=None, help="GitHub token (optional)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sources = {source.strip().lower() for source in args.sources.split(",") if source.strip()}

    results: List[Dict[str, Any]] = []
    if "arxiv" in sources:
        results.extend(fetch_arxiv(args.query, args.limit))
        time.sleep(1)
    if "news" in sources:
        results.extend(fetch_gdelt(args.query, args.limit))
        time.sleep(1)
    if "github" in sources:
        results.extend(fetch_github(args.query, args.limit, args.github_token))

    payload = {
        "query": args.query,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "results": results,
    }
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    print(f"Saved {len(results)} results to {args.output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
