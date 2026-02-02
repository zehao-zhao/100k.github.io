#!/usr/bin/env python3
"""Summarize fetched research results with an open-source API or local LLM."""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List
from urllib.request import Request, urlopen


def _post_json(url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    request = Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urlopen(request, timeout=60) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def call_openai_compatible(api_base: str, api_key: str, model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Summarize the item in 2-3 sentences."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = _post_json(f"{api_base.rstrip('/')}/chat/completions", payload, headers)
    return data["choices"][0]["message"]["content"].strip()


def call_ollama(model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3},
    }
    headers = {"Content-Type": "application/json"}
    data = _post_json("http://localhost:11434/api/generate", payload, headers)
    return data.get("response", "").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="research_results.json", help="Input JSON file")
    parser.add_argument("--output", default="research_summaries.json", help="Output JSON file")
    parser.add_argument(
        "--runtime",
        choices=["open-source", "local"],
        default="local",
        help="LLM runtime",
    )
    parser.add_argument("--model", default="llama3.1:8b", help="Model name")
    parser.add_argument("--api-base", default="https://openrouter.ai/api/v1", help="API base URL")
    parser.add_argument("--api-key", default=os.getenv("OPENROUTER_API_KEY"))
    return parser.parse_args()


def build_prompt(item: Dict[str, Any]) -> str:
    return (
        f"Title: {item.get('title', '')}\n"
        f"Source: {item.get('source', '')}\n"
        f"Summary/Abstract: {item.get('summary', '')}\n"
        f"URL: {item.get('url', '')}"
    )


def main() -> None:
    args = parse_args()

    with open(args.input, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    results: List[Dict[str, Any]] = []
    for item in payload.get("results", []):
        prompt = build_prompt(item)
        if args.runtime == "open-source":
            if not args.api_key:
                raise ValueError("Missing API key for open-source runtime")
            summary = call_openai_compatible(args.api_base, args.api_key, args.model, prompt)
        else:
            summary = call_ollama(args.model, prompt)

        results.append({**item, "llm_summary": summary})

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump({"query": payload.get("query"), "results": results}, handle, indent=2)

    print(f"Saved {len(results)} summaries to {args.output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
