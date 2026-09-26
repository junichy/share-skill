#!/usr/bin/env python3
"""Lightweight gate for SEO article structure packages.

This script checks whether a Markdown research/outline/package file contains
the explicit SEO Article Structure Gate block and enough structural evidence to
proceed. It is intentionally conservative: semantic quality still requires
human/agent judgment, but missing gate artifacts should not slip through.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ARTICLE_TYPES = {
    "definition",
    "duration",
    "howto",
    "anxiety",
    "selection",
    "comparison",
    "normal",
}


CHECKS = [
    "Early answer appears before the first major detour",
    "H2 flow matches the article type or deviation is explained",
    "H3s are scan-friendly decision units",
    "Major H2s have next-link decisions",
    "Reader-path link hub is planned when the article should route choices or next actions",
    "Contextual internal links are planned",
    "Related article / cluster links are planned",
    "CTA placement matches reader intent",
    "Final summary gives one practical next action",
    "Site identity / trust signal is present",
    "Benchmark wording/order/data is not copied",
]


def count_checked(text: str) -> tuple[int, int]:
    checked = len(re.findall(r"(?m)^-\s*\[[xX]\]\s+", text))
    unchecked = len(re.findall(r"(?m)^-\s*\[\s\]\s+", text))
    return checked, unchecked


def h2_count(text: str) -> int:
    return len(re.findall(r"(?m)^##\s+(?!#)", text))


def h3_count(text: str) -> int:
    return len(re.findall(r"(?m)^###\s+", text))


def markdown_link_count(text: str) -> int:
    markdown = len(re.findall(r"\[[^\]]+\]\([^)]+\)", text))
    html = len(re.findall(r"<a\s+[^>]*href=", text, flags=re.I))
    return markdown + html


def table_rows_after_heading(text: str, heading: str) -> int:
    pattern = rf"(?ms)^###\s+{re.escape(heading)}\s*\n(.+?)(?=^###\s+|^##\s+|\Z)"
    match = re.search(pattern, text)
    if not match:
        return 0
    return len([line for line in match.group(1).splitlines() if line.strip().startswith("|")])


def contains_any(text: str, words: list[str]) -> bool:
    return any(word in text for word in words)


def evaluate(path: Path, article_type: str | None) -> tuple[str, list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    warnings: list[str] = []

    if "## SEO Article Structure Gate" not in text:
        failures.append("Missing `## SEO Article Structure Gate` block.")

    if article_type and article_type not in ARTICLE_TYPES:
        failures.append(f"Unknown article type `{article_type}`.")

    checked, unchecked = count_checked(text)
    if checked < 8:
        failures.append(f"Only {checked} checked gate items found; expected at least 8.")
    if unchecked:
        warnings.append(f"{unchecked} unchecked gate item(s) remain.")

    h2s = h2_count(text)
    if h2s < 5:
        warnings.append(f"Only {h2s} H2 headings found; most SEO articles need a fuller H2 flow.")

    h3s = h3_count(text)
    if h3s < 3:
        warnings.append(f"Only {h3s} H3 headings found; confirm H3 scan units are intentionally light.")

    links = markdown_link_count(text)
    if links < 3:
        warnings.append(f"Only {links} Markdown/HTML link(s) found; confirm internal-link plan is explicit.")

    role_rows = table_rows_after_heading(text, "H2 Role Map")
    if role_rows < 4:
        failures.append("H2 Role Map is missing or too sparse.")

    link_rows = table_rows_after_heading(text, "Internal Link Plan")
    if link_rows < 4:
        failures.append("Internal Link Plan is missing or too sparse.")

    reader_path_needed = contains_any(
        text,
        [
            "parent guide",
            "decision-support",
            "service-adjacent",
            "reader-path",
            "Reader-Path",
            "hub",
            "sidebar",
            "サイドバー",
            "関連記事",
            "関連リンク",
            "リンク集",
            "導線",
        ],
    )
    reader_path_present = contains_any(
        text,
        [
            "Reader-Path Link Hub Plan",
            "Reader Path Hub",
            "Universal SEO components used",
            "Condition / audience / location / schedule hub",
            "Related-question block",
            "Bottom cluster links",
            "Trust / operator links",
            "reader journey",
            "読者導線",
            "条件別",
            "ユーザー意図に沿ったリンク",
        ],
    )
    if reader_path_needed and not reader_path_present:
        warnings.append(
            "Reader-path hub signals are present, but no explicit Reader-Path Link Hub Plan was found."
        )

    if not contains_any(text, ["CTA", "next action", "次アクション", "相談", "探す", "問い合わせ"]):
        warnings.append("No obvious CTA or next-action language found.")

    if not contains_any(text, ["Summary", "まとめ", "要点", "結論"]):
        warnings.append("No obvious summary marker found.")

    if not contains_any(text, ["Trust", "信頼", "運営", "監修", "出典", "参考", "会社", "許可"]):
        warnings.append("No obvious trust/site-identity marker found.")

    if failures:
        status = "FAIL"
    elif warnings:
        status = "WARN"
    else:
        status = "PASS"

    return status, failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check SEO article structure artifacts.")
    parser.add_argument("markdown", type=Path, help="Markdown research/outline/package file")
    parser.add_argument("--type", choices=sorted(ARTICLE_TYPES), help="Article type")
    args = parser.parse_args()

    if not args.markdown.exists():
        print(f"FAIL: file not found: {args.markdown}", file=sys.stderr)
        return 2

    status, failures, warnings = evaluate(args.markdown, args.type)
    print(f"SEO Article Structure Gate: {status}")
    if args.type:
        print(f"Article type: {args.type}")

    if failures:
        print("\nFailures:")
        for item in failures:
            print(f"- {item}")

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")

    if status == "PASS":
        return 0
    if status == "WARN":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
