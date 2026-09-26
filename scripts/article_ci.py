#!/usr/bin/env python3
"""Warning-centered SEO check report for article artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


STATUS_ORDER = {"PASS": 0, "WARN": 1, "NEEDS_EVIDENCE": 2, "FAIL": 3}
FAIL_ON_STATUS = {"warn": "WARN", "needs_evidence": "NEEDS_EVIDENCE", "fail": "FAIL"}


@dataclass
class Finding:
    stage: str
    status: str
    check: str
    message: str
    evidence: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "stage": self.stage,
            "status": self.status,
            "check": self.check,
            "message": self.message,
            "evidence": self.evidence,
        }


def read_text(path: Path | None) -> str:
    if not path:
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def contains_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def count_any(text: str, patterns: Iterable[str]) -> int:
    return sum(1 for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE))


def is_placeholder_value(text: str) -> bool:
    value = normalize(strip_tags(text)).strip(" -:：")
    if not value:
        return True
    placeholder_patterns = [
        r"^<[^>]+>$",
        r"^primary browser snapshot / tool snapshot$",
        r"^parent / child / mixed / unknown$",
        r"^high / medium / low$",
        r"^write / rewrite existing URL / split / merge / retarget / defer$",
        r"^parent / child / mixed / unknown action$",
        r"^\(none\)$",
    ]
    return contains_any(value, placeholder_patterns)


def has_meaningful_text(text: str) -> bool:
    value = normalize(strip_tags(text))
    if is_placeholder_value(value):
        return False
    return bool(re.search(r"https?://|[A-Za-z0-9]{3,}|[ぁ-んァ-ヶ一-龠]{2,}", value))


def markdown_table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return []
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
        return []
    return cells


def meaningful_rank_rows(text: str, start: int = 1, end: int = 20) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        cells = markdown_table_cells(line)
        if not cells:
            continue
        try:
            rank = int(cells[0])
        except ValueError:
            continue
        if start <= rank <= end and any(has_meaningful_text(cell) for cell in cells[1:]):
            rows.append(cells)
    return rows


def section_text(text: str, heading_pattern: str) -> str:
    match = re.search(rf"(?is)^##\s*{heading_pattern}\s*(.*?)(?=^##\s+|\Z)", text, flags=re.M)
    return match.group(1) if match else ""


def labeled_value(text: str, label_pattern: str) -> str:
    match = re.search(rf"(?im)^\s*(?:[-*]\s*)?(?:{label_pattern})\s*[:：]\s*(.*?)\s*$", text)
    return match.group(1).strip() if match else ""


def labeled_block_has_content(text: str, label_pattern: str) -> bool:
    lines = text.splitlines()
    label_re = re.compile(rf"^\s*(?:[-*]\s*)?(?:{label_pattern})\s*[:：]\s*(.*?)\s*$", re.I)
    next_label_re = re.compile(r"^\s*(?:[-*]\s*)?(?:[A-Za-z][A-Za-z /-]{2,}|[\w一-龠ぁ-んァ-ヶ]+)\s*[:：]\s*")
    for index, line in enumerate(lines):
        match = label_re.match(line)
        if not match:
            continue
        if has_meaningful_text(match.group(1)):
            return True
        for following in lines[index + 1 :]:
            if following.startswith("#"):
                break
            if next_label_re.match(following) and not following.startswith((" ", "\t")):
                break
            if has_meaningful_text(following):
                return True
        return False
    return False


def section_has_meaningful_content(text: str, heading_pattern: str) -> bool:
    section = section_text(text, heading_pattern)
    if not section:
        return False
    meaningful_lines = [
        line
        for line in section.splitlines()
        if has_meaningful_text(line)
        and not markdown_table_cells(line)
        and not re.match(r"^\s*(?:[-*]\s*)?.+[:：]\s*$", line)
    ]
    return bool(meaningful_lines)


def strip_tags(text: str) -> str:
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(normalize(text))


def markdown_headings(text: str, level: int) -> list[str]:
    pattern = rf"(?m)^#{{{level}}}\s+(.+?)\s*$"
    return [normalize(match) for match in re.findall(pattern, text)]


def html_headings(text: str, level: int) -> list[str]:
    pattern = rf"<h{level}\b[^>]*>(.*?)</h{level}>"
    return [strip_tags(match) for match in re.findall(pattern, text, flags=re.I | re.S)]


def headings(text: str, level: int) -> list[str]:
    return markdown_headings(text, level) + html_headings(text, level)


def title_candidates(text: str) -> list[str]:
    titles = headings(text, 1)
    titles += [strip_tags(match) for match in re.findall(r"<title\b[^>]*>(.*?)</title>", text, flags=re.I | re.S)]
    yaml_title = re.search(r"(?m)^title:\s*[\"']?(.+?)[\"']?\s*$", text)
    if yaml_title:
        titles.append(normalize(yaml_title.group(1)))
    return [title for title in titles if title]


def first_content_block(text: str) -> str:
    without_frontmatter = re.sub(r"\A---.*?---", "", text, flags=re.S).strip()
    without_h1 = re.sub(r"(?m)^#\s+.+?$", "", without_frontmatter, count=1).strip()
    before_h2 = re.split(r"(?m)^##\s+", without_h1, maxsplit=1)[0]
    return strip_tags(before_h2)[:1200]


def rank_evidence_count(text: str) -> int:
    rank_patterns = [
        r"(?m)^\s*(?:rank|順位)\s*[:：]?\s*\d{1,2}\b.+\S",
        r"(?m)^\s*#{2,4}\s*(?:rank\s*)?\d{1,2}[\).、:：\s]",
    ]
    count = sum(len(re.findall(pattern, text, flags=re.I)) for pattern in rank_patterns)
    count += len(meaningful_rank_rows(text))
    urls = len(re.findall(r"https?://[^\s)>\"]+", text))
    return max(count, min(urls, 20))


def topic_judgment_section(text: str) -> str:
    match = re.search(
        r"(?is)##\s*Parent\s*/\s*Child\s*Topic\s*Judgment\s*(.*?)(?=\n##\s+|\Z)",
        text,
    )
    return match.group(1) if match else ""


def structure_rationale_section(text: str) -> str:
    patterns = [
        r"Top\s*10\s*(?:->|→|to)\s*Article\s*Structure\s*Rationale",
        r"Article\s*Structure\s*Rationale",
        r"SERP\s*(?:to|->|→)\s*(?:Article\s*)?Structure",
        r"上位\s*10\s*件.*(?:構成|見出し).*(?:理由|根拠)",
        r"構成(?:理由|根拠)",
    ]
    for pattern in patterns:
        section = section_text(text, pattern)
        if section:
            return section
    return ""


def title_top10_comparison_section(text: str) -> str:
    patterns = [
        r"Title\s*Top\s*10\s*Comparison",
        r"Top\s*10\s*Title\s*Comparison",
        r"タイトル.*(?:上位|Top)\s*10.*(?:比較|comparison)",
    ]
    for pattern in patterns:
        section = section_text(text, pattern)
        if section:
            return section
    return ""


def structure_top10_comparison_section(text: str) -> str:
    patterns = [
        r"Structure\s*Top\s*10\s*Comparison",
        r"Top\s*10\s*Structure\s*Comparison",
        r"(?:構成|見出し).*(?:上位|Top)\s*10.*(?:比較|comparison)",
    ]
    for pattern in patterns:
        section = section_text(text, pattern)
        if section:
            return section
    return ""


def comparison_strength(section: str, axis_patterns: Iterable[str]) -> tuple[int, int, int]:
    if not section:
        return (0, 0, 0)
    rows = meaningful_rank_rows(section, 1, 10)
    rank_hits = len(rows) or count_any(
        section,
        [
            r"rank\s*(?:[1-9]|10)\b",
            r"(?:[1-9]|10)\s*位",
            r"\|\s*(?:[1-9]|10)\s*\|",
        ],
    )
    axis_hits = count_any(section, axis_patterns)
    decision_hits = count_any(section, [r"adopt|avoid|採用|不採用|copy|avoid|深く|薄く|internal-link|内部リンク|CTA|導線|決定|decision"])
    return (rank_hits, axis_hits, decision_hits)


def has_explicit_topic_classification(text: str) -> bool:
    section = topic_judgment_section(text) or text
    value = labeled_value(section, r"(?:Classification|分類)")
    if not value or is_placeholder_value(value):
        return False
    return contains_any(value, [r"^(?:parent|child|mixed|unknown)\b", r"^(?:親|子|混在|不明)"])


def topic_evidence_strength(text: str) -> int:
    section = topic_judgment_section(text) or text
    axes = [
        r"SERP breadth",
        r"Rank ladder",
        r"Lower-page comparison",
        r"SERP features",
        r"Query variants? that likely belong inside this page|Query variants? inside top pages",
        r"Query variants? that likely need separate pages|Query variants? needing separate pages",
        r"GSC query spread",
    ]
    hits = sum(1 for label in axes if labeled_block_has_content(section, label))
    if hits:
        return hits
    return count_any(section, [r"top\s*10|上位", r"順位", r"子KW|親KW|クエリ", r"GSC|Search Console|表示回数|impressions"])


def structure_rationale_strength(text: str) -> tuple[int, int, int]:
    section = structure_rationale_section(text)
    if not section:
        return (0, 0, 0)
    evidence_hits = count_any(
        section,
        [
            r"rank\s*(?:[1-9]|10)\b",
            r"(?:[1-9]|10)\s*位",
            r"top\s*(?:[1-9]|10|3|5)",
            r"上位\s*(?:[1-9]|10|3|5)",
            r"競合",
            r"SERP",
        ],
    )
    structure_hits = count_any(section, [r"\bH[23]\b", r"見出し", r"section", r"セクション", r"構成"])
    decision_hits = count_any(section, [r"include|exclude|adopt|defer|split|merge", r"採用|入れる|入れた|見送り|分ける|厚く|薄く|理由|根拠|反映"])
    return (evidence_hits, structure_hits, decision_hits)


def top10_unreadable_reason_count(text: str) -> int:
    section = section_text(text, r"Organic Top 10|Top 10|Organic top results")
    unreadable = section_text(text, r"Unreadable ranks|Unconfirmed ranks|未確認順位|確認不能順位")
    combined = "\n".join(part for part in [section, unreadable] if part)
    return len(
        re.findall(
            r"(?im)^\s*(?:[-*]\s*)?(?:rank\s*)?(?:10|[1-9])(?:位)?\s*[:：-]\s*(?!\s*$).+",
            combined,
        )
    )


def has_topic_action_branch(text: str) -> bool:
    section = topic_judgment_section(text) or text
    return contains_any(section, [r"Decision branch|action branch|対応分岐|Decision\s*:"]) and contains_any(
        section,
        [
            r"pillar|hub|cluster|internal link|split|merge|retarget|broad guide",
            r"親|子|内部リンク|ハブ|カテゴリ|専用記事|分割|統合|リライト|既存URL",
        ],
    )


def query_terms(query: str) -> list[str]:
    terms = [term.strip() for term in re.split(r"[\s　]+", query) if term.strip()]
    return terms[:8]


def compact_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def status_summary(findings: list[Finding]) -> dict[str, int]:
    summary = {status: 0 for status in STATUS_ORDER}
    for finding in findings:
        summary[finding.status] += 1
    return summary


def overall_status(findings: list[Finding]) -> str:
    if not findings:
        return "PASS"
    return max((finding.status for finding in findings), key=lambda status: STATUS_ORDER[status])


def parse_profile_scalar(value: str) -> object:
    cleaned = value.strip().strip("\"'")
    if re.fullmatch(r"-?\d+", cleaned):
        return int(cleaned)
    if cleaned.lower() in {"true", "false"}:
        return cleaned.lower() == "true"
    return cleaned


def load_site_profile(path: Path | None) -> dict[str, object]:
    if not path:
        return {}
    raw = read_text(path)
    if not raw.strip():
        return {}
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}

    profile: dict[str, object] = {}
    for line in raw.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key and value:
            profile[key] = parse_profile_scalar(value)
    return profile


def profile_int(profile: dict[str, object], keys: Iterable[str], default: int) -> int:
    for key in keys:
        value = profile.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and re.fullmatch(r"-?\d+", value.strip()):
            return int(value.strip())
    return default


def add(findings: list[Finding], stage: str, status: str, check: str, message: str, evidence: str = "") -> None:
    findings.append(Finding(stage=stage, status=status, check=check, message=message, evidence=evidence))


def unsafe_ymyl_hits(text: str) -> list[str]:
    unsafe_patterns = [
        r"必ず治る",
        r"絶対に大丈夫",
        r"病院に行かなくてよい",
        r"自己判断で.{0,40}(?:薬|吐かせ)",
        r"無理に吐かせ(?:る|ましょう)",
        r"吐かせましょう",
        r"様子を見れば(?:大丈夫|よい)",
    ]
    safe_context_patterns = [
        r"せず",
        r"しない",
        r"ないで",
        r"ならない",
        r"とは限りません",
        r"危険",
        r"指示",
        r"連絡",
        r"相談",
    ]
    hits: list[str] = []
    for pattern in unsafe_patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.S):
            snippet = text[max(0, match.start() - 40) : min(len(text), match.end() + 40)]
            if contains_any(snippet, safe_context_patterns):
                continue
            hits.append(normalize(snippet))
    return hits


def research_ci(findings: list[Finding], research_texts: list[str], target_query: str) -> None:
    stage = "Research CI"
    combined = "\n\n".join(research_texts)
    if not combined.strip():
        add(findings, stage, "NEEDS_EVIDENCE", "SERP evidence", "No research file was provided.")
        return

    if target_query or contains_any(combined, [r"target query", r"query\s*[:：]", r"対象\s*query", r"検索クエリ", r"メインKW"]):
        add(findings, stage, "PASS", "Target query", "Target query evidence is present.", target_query)
    else:
        add(findings, stage, "NEEDS_EVIDENCE", "Target query", "Target query is not explicit in arguments or research.")

    snapshot_hits = 0
    if labeled_block_has_content(combined, r"Date|日付"):
        snapshot_hits += 1
    if labeled_block_has_content(combined, r"Google URL|Source reference / export"):
        snapshot_hits += 1
    if labeled_block_has_content(combined, r"q"):
        snapshot_hits += 1
    if labeled_block_has_content(combined, r"hl / gl / pws|hl|gl|pws"):
        snapshot_hits += 1
    if labeled_block_has_content(combined, r"Location / personalization|location|personalization|地域|パーソナライズ"):
        snapshot_hits += 1
    if snapshot_hits >= 3:
        add(findings, stage, "PASS", "SERP snapshot metadata", "Query URL, date, location, or personalization evidence is present.")
    else:
        add(findings, stage, "WARN", "SERP snapshot metadata", "Record exact query, date, source reference and available settings; Google q/start/context apply only to browser snapshots.")

    if contains_any(
        combined,
        [
            r"Computer Use",
            r"user Chrome",
            r"ユーザー.*Chrome",
            r"primary browser snapshot",
            r"実ブラウザ",
            r"実SERP",
            r"Search source\s*[:：]\s*(?:approved keyword source|keyword source|browser)",
        ],
    ):
        add(findings, stage, "PASS", "Primary SERP source", "Research records an approved keyword source or actual-browser SERP source; verify its referenced artifact.")
    else:
        add(findings, stage, "WARN", "Primary SERP source", "Record the actual keyword-source feature/source or observed browser source, not a search-summary guess.")

    if contains_any(
        combined,
        [
            r"Organic rank exclusion notes",
            r"organic rank.*除外",
            r"rank.*除外",
            r"広告.*(?:除外|not counted)",
            r"AI Overview.*(?:除外|not counted)",
            r"PAA.*(?:除外|not counted)",
            r"sitelinks?|サイトリンク",
            r"duplicate URL fragments?|同一URL.*フラグメント|#:~:text",
        ],
    ):
        add(findings, stage, "PASS", "Organic-rank exclusion notes", "Research records which SERP modules were not counted as organic ranks.")
    else:
        add(findings, stage, "WARN", "Organic-rank exclusion notes", "Record ads, AIO, PAA, snippets, packs, sitelinks, and same-URL fragments that were excluded from organic rank.")

    if labeled_block_has_content(combined, r"Candidate volume / difficulty") or contains_any(
        combined, [r"月間検索(?:数|ボリューム)\s*[:：]?\s*\d+", r"(?:volume|検索数|難易度)\s*[:：]\s*\S+"]
    ):
        add(findings, stage, "PASS", "Candidate volume context", "Volume or difficulty context is present.")
    else:
        add(findings, stage, "WARN", "Candidate volume context", "If this is candidate selection, add volume/difficulty context; for pure rewrites, record why it is skipped.")

    rank_count = rank_evidence_count(combined)
    if rank_count >= 10:
        add(findings, stage, "PASS", "Top-page coverage", f"Found evidence for about {rank_count} ranked pages.")
    elif rank_count >= 8:
        add(findings, stage, "WARN", "Top-page coverage", f"Found evidence for about {rank_count} ranked pages; top 10 is preferred.")
    elif rank_count >= 5:
        add(findings, stage, "WARN", "Top-page coverage", f"Found evidence for about {rank_count} ranked pages; top 10 is the new default.")
    else:
        add(findings, stage, "NEEDS_EVIDENCE", "Top-page coverage", "Top-page evidence is too thin for an SEO decision.", f"rank/page evidence count: {rank_count}")

    top10_rows = meaningful_rank_rows(combined, 1, 10)
    top10_confirmed = {int(row[0]) for row in top10_rows if row and row[0].isdigit()}
    missing_top10 = [str(rank) for rank in range(1, 11) if rank not in top10_confirmed]
    unreadable_reasons = top10_unreadable_reason_count(combined)
    if len(top10_confirmed) >= 10:
        add(findings, stage, "PASS", "Organic top 10 completeness", "All organic top 10 ranks have row-level evidence.")
    elif len(top10_confirmed) + unreadable_reasons >= 10:
        add(
            findings,
            stage,
            "WARN",
            "Organic top 10 completeness",
            "Some top-10 ranks are not fully inspected but unreadable/unconfirmed reasons are recorded.",
            f"confirmed={len(top10_confirmed)}, reasoned={unreadable_reasons}, missing={','.join(missing_top10)}",
        )
    elif len(top10_confirmed) >= 8:
        add(
            findings,
            stage,
            "WARN",
            "Organic top 10 completeness",
            "Top 10 is incomplete. Inspect every organic rank 1-10 or record a concrete reason for each missing rank.",
            f"confirmed={len(top10_confirmed)}, missing={','.join(missing_top10)}",
        )
    else:
        add(
            findings,
            stage,
            "NEEDS_EVIDENCE",
            "Organic top 10 completeness",
            "Organic top 10 evidence is too incomplete for structure decisions.",
            f"confirmed={len(top10_confirmed)}, missing={','.join(missing_top10)}",
        )

    structured_rows = [
        row
        for row in meaningful_rank_rows(combined, 1, 10)
        if sum(1 for cell in row[1:] if has_meaningful_text(cell)) >= 3
    ]
    if len(structured_rows) >= 5:
        add(findings, stage, "PASS", "Structure evidence", "Research includes page structure and winning-pattern clues.")
    elif len(structured_rows) >= 1:
        add(findings, stage, "WARN", "Structure evidence", "Some ranked pages include structure evidence, but top-page structure is still thin.")
    else:
        add(findings, stage, "WARN", "Structure evidence", "Research should include title, H1, H2/H3, page type, CTA, and winning reason.")

    top5_deep_rows = [
        row
        for row in meaningful_rank_rows(combined, 1, 5)
        if sum(1 for cell in row[1:] if has_meaningful_text(cell)) >= 5
    ]
    if len(top5_deep_rows) >= 5:
        add(findings, stage, "PASS", "Top 5 deep inspection", "Top 5 pages include deeper title/H1/H2/answer/CTA-style evidence.")
    elif len(top5_deep_rows) >= 3:
        add(findings, stage, "WARN", "Top 5 deep inspection", "Some top 5 pages have depth, but inspect every top result before deciding title or outline.")
    else:
        add(findings, stage, "WARN", "Top 5 deep inspection", "Top 5 pages should be inspected beyond URL/title: H2/H3, immediate answer, CTA, trust, examples, question blocks when present, and media.")

    if section_has_meaningful_content(combined, r"Page Type Mix") or contains_any(
        combined,
        [
            r"page type mix",
            r"優勢な page type",
            r"Dominant winning page type",
            r"記事.*LP.*(?:一覧|カテゴリ|Q&A|動画)",
        ],
    ):
        add(findings, stage, "PASS", "Page type mix", "Research records the mix of winning SERP page types.")
    else:
        add(findings, stage, "WARN", "Page type mix", "Record whether top results are articles, LPs, category/list pages, Q&A, official/company pages, video/image-heavy pages, or another type.")

    feature_section = section_text(combined, r"SERP Features")
    feature_hits = sum(
        1
        for label in [r"Ads", r"AI Overview", r"Featured snippet", r"PAA", r"Video pack", r"Image pack", r"Local/map", r"Other"]
        if labeled_block_has_content(feature_section, label)
    )
    if feature_hits >= 2:
        add(findings, stage, "PASS", "SERP features", "SERP feature evidence is present.")
    else:
        add(findings, stage, "WARN", "SERP features", "Record source-labelled AIO/PAA/video/image/ad observations; unobserved does not mean absent.")

    topic_section = topic_judgment_section(combined)
    if has_explicit_topic_classification(combined):
        add(findings, stage, "PASS", "Topic classification", "Parent/child/mixed/unknown classification is explicit.")
    elif labeled_value(topic_section or combined, r"(?:Classification|分類)"):
        add(findings, stage, "WARN", "Topic classification", "Topic classification field is still a placeholder or unclear.")
    elif contains_any(combined, [r"親トピック", r"子トピック", r"\bpillar\b", r"\bchild\b", r"parent topic"]):
        add(findings, stage, "WARN", "Topic classification", "Topic role is mentioned, but the classification label should be explicit.")
    else:
        add(findings, stage, "WARN", "Topic classification", "Parent-topic vs child-topic classification is not explicit.")

    topic_evidence_hits = topic_evidence_strength(combined)
    if topic_section and topic_evidence_hits >= 4:
        add(findings, stage, "PASS", "Topic classification evidence", "Classification is supported by SERP/GSC-style evidence.")
    elif topic_section and topic_evidence_hits >= 2:
        add(findings, stage, "WARN", "Topic classification evidence", "Classification evidence is present but should cover more axes.", f"evidence axes: {topic_evidence_hits}")
    else:
        add(findings, stage, "WARN", "Topic classification evidence", "Support topic classification with SERP breadth, rank ladder, lower-page and 20-30 fallen-page comparison, SERP features, query variants, and GSC when available.")

    if has_topic_action_branch(combined):
        add(findings, stage, "PASS", "Topic strategy branch", "Topic label is tied to a concrete action branch.")
    else:
        add(findings, stage, "WARN", "Topic strategy branch", "Tie the parent/child/mixed/unknown label to an action: pillar/hub, focused child article, split/retarget, internal links, or evidence collection.")

    ladder_patterns = [
        r"10\s*(?:位|->|→)\s*1",
        r"rank ladder",
        r"順位差",
        r"順位づけ",
        r"登る",
        r"top\s*10\s*(?:vs|と)\s*top\s*5",
        r"top\s*5\s*(?:vs|と)\s*top\s*3",
        r"1\s*位.*理由",
    ]
    if contains_any(combined, ladder_patterns) and section_has_meaningful_content(combined, r"Rank Ladder"):
        add(findings, stage, "PASS", "Rank ladder analysis", "Research explains what changes as pages climb from 10 to 1.")
    else:
        add(findings, stage, "WARN", "Rank ladder analysis", "Add a 10 -> 1 comparison: what top 5/top 3/rank 1 add beyond lower top-10 pages.")

    title_rank_hits, title_axis_hits, title_decision_hits = comparison_strength(
        title_top10_comparison_section(combined),
        [
            r"subject|主語",
            r"front-loaded|前半",
            r"condition|条件",
            r"anxiety|不安",
            r"solution|解決",
            r"naturalness|自然",
            r"intent fit|検索意図",
        ],
    )
    if title_rank_hits >= 8 and title_axis_hits >= 3 and title_decision_hits >= 2:
        add(findings, stage, "PASS", "Title top 10 comparison", "Research compares top-10 titles before deciding the article title.")
    elif title_rank_hits or title_axis_hits or title_decision_hits:
        add(
            findings,
            stage,
            "WARN",
            "Title top 10 comparison",
            "Title comparison is present but should compare more top-10 titles and explain adopt/avoid decisions.",
            f"ranks={title_rank_hits}, axes={title_axis_hits}, decisions={title_decision_hits}",
        )
    else:
        add(findings, stage, "WARN", "Title top 10 comparison", "Add a top-10 title comparison before deciding the article title.")

    structure_rank_hits, structure_axis_hits, structure_decision_hits = comparison_strength(
        structure_top10_comparison_section(combined),
        [
            r"H1|H2|H3|見出し",
            r"opening answer|即答",
            r"must-have|必須",
            r"question block|質問ブロック|PAA",
            r"media|image|gallery|画像|ギャラリー",
            r"CTA|導線",
            r"examples|tables|例|表",
        ],
    )
    if structure_rank_hits >= 8 and structure_axis_hits >= 3 and structure_decision_hits >= 2:
        add(findings, stage, "PASS", "Structure top 10 comparison", "Research compares top-10 structures before deciding the outline.")
    elif structure_rank_hits or structure_axis_hits or structure_decision_hits:
        add(
            findings,
            stage,
            "WARN",
            "Structure top 10 comparison",
            "Structure comparison is present but should compare more top-10 H1/H2/H3 patterns and decisions.",
            f"ranks={structure_rank_hits}, axes={structure_axis_hits}, decisions={structure_decision_hits}",
        )
    else:
        add(findings, stage, "WARN", "Structure top 10 comparison", "Add a top-10 structure comparison before deciding the outline.")

    if section_has_meaningful_content(combined, r"Winning Structure Decision") or contains_any(
        structure_rationale_section(combined), [r"Final H2|最終 H2|勝ち筋|winning structure|相談導線|service page"]
    ):
        add(findings, stage, "PASS", "Winning structure decision", "Research states the structure decision derived from top-10 comparison.")
    else:
        add(findings, stage, "WARN", "Winning structure decision", "State the final H2/H3 order, section depth, internal-link outs, and CTA placement before drafting.")

    structure_evidence_hits, structure_hits, decision_hits = structure_rationale_strength(combined)
    if structure_evidence_hits >= 3 and structure_hits >= 2 and decision_hits >= 2:
        add(findings, stage, "PASS", "Top-10-to-structure rationale", "Research explains how top-10 SERP evidence became the article structure.")
    elif structure_evidence_hits or structure_hits or decision_hits:
        add(
            findings,
            stage,
            "WARN",
            "Top-10-to-structure rationale",
            "Structure rationale is present but should explicitly map top-10 observations to included/excluded H2/H3 decisions.",
            f"evidence={structure_evidence_hits}, structure={structure_hits}, decisions={decision_hits}",
        )
    else:
        add(
            findings,
            stage,
            "WARN",
            "Top-10-to-structure rationale",
            "Add a section that maps each major H2/H3 decision to top-10 SERP evidence and explains what was included, excluded, or split.",
        )

    if meaningful_rank_rows(combined, 11, 20) or section_has_meaningful_content(combined, r"Lower-Page Comparison"):
        add(findings, stage, "PASS", "Around-20 lower-page comparison", "Research includes lower-page comparison around ranks 11 to 20.")
    else:
        add(findings, stage, "WARN", "Around-20 lower-page comparison", "Inspect around ranks 11 -> 20 when feasible and record why similar pages are lower.")

    fallen_rows = meaningful_rank_rows(combined, 20, 30)
    if len(fallen_rows) >= 3 or section_has_meaningful_content(combined, r"Fallen-Page Comparison|20\s*(?:->|→)\s*30|20\s*位.*30\s*位"):
        add(findings, stage, "PASS", "Fallen-page comparison 20-30", "Research explains why pages around ranks 20-30 are not reaching the top 10.")
    else:
        add(
            findings,
            stage,
            "WARN",
            "Fallen-page comparison 20-30",
            "Inspect ranks 20-30 and record why they fall below the top 10, especially pages similar to the planned article.",
        )

    intent_section = section_text(combined, r"Intent-Fit Comparison")
    has_standard_answer = section_has_meaningful_content(combined, r"SERP Standard Answer")
    has_mismatch = labeled_block_has_content(intent_section, r"Mismatch risk|主題ズレ")
    has_decision = labeled_block_has_content(intent_section, r"Decision|判断")
    if has_standard_answer and has_mismatch and has_decision:
        add(findings, stage, "PASS", "Intent-fit comparison", "SERP answer, mismatch risk, and decision are present.")
    else:
        add(findings, stage, "WARN", "Intent-fit comparison", "Research should state SERP standard answer, mismatch risk, and decision together.")


def draft_ci(findings: list[Finding], article_text: str, has_research: bool, target_query: str, site_profile: dict[str, object]) -> None:
    stage = "Draft CI"
    if not article_text.strip():
        add(findings, stage, "FAIL", "Article input", "No article file was provided.")
        return

    titles = title_candidates(article_text)
    title = titles[0] if titles else ""
    if title:
        add(findings, stage, "PASS", "Title/H1 presence", "Title or H1 is present.", title)
    else:
        add(findings, stage, "FAIL", "Title/H1 presence", "No title or H1 was found.")

    if title and re.search(r"[|｜:：\-–—]| {2,}", title):
        add(findings, stage, "WARN", "Natural title", "Title may read like joined keywords or a stitched SEO title.", title)
    elif title:
        add(findings, stage, "PASS", "Natural title", "Title does not show obvious separator-heavy keyword stitching.")

    if title:
        title_len = compact_len(title)
        min_chars = profile_int(site_profile, ["title_min_chars", "title_length_min", "title_min"], 24)
        max_chars = profile_int(site_profile, ["title_max_chars", "title_length_max", "title_max"], 42)
        if max_chars < min_chars:
            min_chars = 0
        if min_chars <= title_len <= max_chars:
            add(findings, stage, "PASS", "Title length", f"Title length looks intentional for SEO display.", f"{title_len} chars; allowed {min_chars}-{max_chars}")
        else:
            add(findings, stage, "WARN", "Title length", "Confirm the title is not too vague, too short, or too long for the SERP.", f"{title_len} chars; allowed {min_chars}-{max_chars}")

    terms = query_terms(target_query)
    if title and terms:
        missing_terms = [term for term in terms if term not in title]
        if not missing_terms:
            add(findings, stage, "PASS", "Target-query visibility", "Core query terms are visible in the title.", ", ".join(terms))
        elif len(missing_terms) < len(terms):
            add(findings, stage, "WARN", "Target-query visibility", "Some target-query terms are not visible in the title; confirm semantic coverage.", ", ".join(missing_terms))
        else:
            add(findings, stage, "WARN", "Target-query visibility", "Target-query terms are not visible in the title; confirm this is intentional.", ", ".join(missing_terms))

    h2s = headings(article_text, 2)
    h3s = headings(article_text, 3)
    if len(h2s) >= 4:
        add(findings, stage, "PASS", "Heading depth", f"Found {len(h2s)} H2 headings and {len(h3s)} H3 headings.")
    elif len(h2s) >= 2:
        add(findings, stage, "WARN", "Heading depth", f"Only {len(h2s)} H2 headings found; confirm SERP parity.")
    else:
        add(findings, stage, "WARN", "Heading depth", "Article has very little scannable H2 structure.")

    lead = first_content_block(article_text)
    if contains_any(lead, [r"まず", r"確認", r"相談", r"電話", r"受診", r"結論", r"最初"]):
        add(findings, stage, "PASS", "Immediate answer", "Lead appears to give an early practical answer.")
    else:
        add(findings, stage, "WARN", "Immediate answer", "Lead may not answer the worried user's next action early enough.")

    if title and lead:
        alignment_terms = [
            r"誤飲",
            r"確認",
            r"対処",
            r"受診",
            r"相談",
            r"連絡",
            r"吐かせ",
            r"何を",
            r"いつ",
            r"どれくらい",
        ]
        title_hits = [term for term in alignment_terms if re.search(term, title)]
        lead_hits = [term for term in alignment_terms if re.search(term, lead)]
        shared = set(title_hits) & set(lead_hits)
        if len(shared) >= 2 or (terms and all(term in lead for term in terms)):
            add(findings, stage, "PASS", "Title/lead alignment", "Lead appears to continue the same topic as the title.")
        else:
            add(findings, stage, "WARN", "Title/lead alignment", "Lead may not repeat or answer the title's main promise clearly.")

    link_count = len(re.findall(r"\[[^\]]+\]\([^)]+\)|<a\b[^>]*href=", article_text, flags=re.I))
    if link_count >= 2:
        add(findings, stage, "PASS", "Internal/external links", f"Found {link_count} markdown or HTML links.")
    elif link_count == 1:
        add(findings, stage, "WARN", "Internal links", "Only one link found; cluster support may be thin.")
    else:
        add(findings, stage, "WARN", "Internal links", "No links found; article may not be connected to a cluster.")

    ymyl_context = contains_any(article_text, [r"症状", r"治療", r"受診", r"薬", r"救急", r"病院", r"医師", r"獣医", r"法律", r"税務", r"投資"])
    unsafe_hits = unsafe_ymyl_hits(article_text) if ymyl_context else []
    if unsafe_hits:
        add(findings, stage, "FAIL", "YMYL safety", "Potentially unsafe professional/medical wording was found.", " / ".join(unsafe_hits[:3]))
    elif ymyl_context:
        add(findings, stage, "PASS", "YMYL safety", "No obvious unsafe wording pattern was found.")

    if has_research:
        add(findings, stage, "PASS", "Research linkage", "Draft can be compared with provided research.")
    else:
        add(findings, stage, "NEEDS_EVIDENCE", "Research linkage", "Draft was checked without SERP research evidence.")


def package_shape(package_text: str, package_path: Path | None) -> str:
    suffix = package_path.suffix.lower() if package_path else ""
    if contains_any(package_text, [r"<html\b", r"<head\b", r"<title\b", r"name=[\"']description[\"']", r"application/ld\+json"]):
        return "full_html"
    if suffix in {".html", ".htm"} and contains_any(package_text, [r"<h[1-6]\b", r"<p\b", r"<figure\b", r"<iframe\b", r"<img\b", r"<table\b", r"<a\b"]):
        return "body_only_wp_html"
    if suffix in {".md", ".markdown"} or contains_any(package_text, [r"(?m)^#{1,3}\s+", r"(?m)^[-*]\s+", r"```"]):
        return "markdown_package"
    return "unknown"


def package_ci(findings: list[Finding], package_text: str, package_path: Path | None) -> None:
    stage = "Package / WP CI"
    if not package_text.strip():
        add(findings, stage, "NEEDS_EVIDENCE", "Package input", "No WordPress/package file was provided.")
        return

    shape = package_shape(package_text, package_path)
    body_only_package = shape == "body_only_wp_html"
    markdown_package = shape == "markdown_package"

    if body_only_package:
        add(findings, stage, "PASS", "Package shape", "Package appears to be body-only WordPress content; title/meta/schema should be verified via CMS or live HTML.")
    elif markdown_package:
        add(findings, stage, "WARN", "Package shape", "Package appears to be markdown package notes, not WordPress HTML. Use actual wp.html for package checks or pass this as --article when it is a draft.")
    elif shape == "unknown":
        add(findings, stage, "WARN", "Package shape", "Package format is unclear; confirm this is WordPress-ready content and not an operations note.")
    elif shape == "full_html":
        add(findings, stage, "PASS", "Package shape", "Package appears to include full HTML metadata.")

    if body_only_package:
        pass
    elif title_candidates(package_text):
        add(findings, stage, "PASS", "Title/H1", "Package includes title or H1 evidence.", title_candidates(package_text)[0])
    else:
        add(findings, stage, "WARN", "Title/H1", "Package does not expose a title or H1.")

    if body_only_package:
        add(findings, stage, "PASS", "Description", "Skipped for body-only package; verify meta description through CMS/live HTML.")
    elif markdown_package:
        add(findings, stage, "WARN", "Description", "Markdown package notes cannot prove meta description output. Use wp.html, CMS fields, or live HTML for this check.")
    elif contains_any(package_text, [r"name=[\"']description[\"']", r"property=[\"']og:description[\"']", r"meta description", r"excerpt", r"抜粋"]):
        add(findings, stage, "PASS", "Description", "Description or excerpt evidence is present.")
    else:
        add(findings, stage, "WARN", "Description", "Meta description or excerpt evidence was not found in the package.")

    if body_only_package:
        add(findings, stage, "PASS", "CMS metadata checklist", "Skipped for body-only package; verify slug/canonical/author/category/dateModified through CMS/live HTML.")
    elif markdown_package:
        add(findings, stage, "WARN", "CMS metadata checklist", "Markdown package notes cannot prove slug/canonical/author/category/dateModified output. Use wp.html, CMS fields, or live HTML for this check.")
    elif contains_any(package_text, [r"rel=[\"']canonical[\"']", r"canonical", r"slug", r"dateModified", r"modified", r"author", r"category", r"カテゴリ"]):
        add(findings, stage, "PASS", "CMS metadata checklist", "Canonical/slug/date/author/category evidence is present.")
    else:
        add(findings, stage, "WARN", "CMS metadata checklist", "Canonical, slug, author, category, or modified date should be checked before publish.")

    if body_only_package:
        add(findings, stage, "PASS", "Schema", "Skipped for body-only package; verify schema through CMS/plugin/live HTML.")
    elif markdown_package:
        add(findings, stage, "WARN", "Schema", "Markdown package notes cannot prove schema output. Use wp.html, CMS/plugin output, or live HTML for this check.")
    elif contains_any(package_text, [r"application/ld\+json", r"schema", r"BlogPosting", r"Article", r"構造化データ"]):
        add(findings, stage, "PASS", "Schema", "Schema evidence is present.")
    else:
        add(findings, stage, "WARN", "Schema", "Schema evidence was not found; confirm CMS/plugin output.")

    if contains_any(package_text, [r"<iframe\b", r"<img\b", r"<table\b", r"<a\b"]):
        add(findings, stage, "PASS", "Rich elements", "Package includes links, embeds, images, or tables.")
    else:
        add(findings, stage, "WARN", "Rich elements", "No links, embeds, images, or tables were found in the package.")

    if contains_any(package_text, [r"TODO", r"FIXME", r"example\.com", r"ここに"]):
        add(findings, stage, "FAIL", "Placeholders", "Placeholder text appears to remain in the package.")


def post_publish_ci(findings: list[Finding], research_texts: list[str], live_url: str, target_query: str) -> None:
    stage = "Post-publish Observation CI"
    combined = "\n\n".join(research_texts)
    has_observation = contains_any(combined, [r"\bGSC\b", r"Search Console", r"表示回数", r"クリック", r"impressions?", r"average position", r"平均掲載順位", r"順位"])
    if live_url or has_observation:
        add(findings, stage, "PASS", "Observation evidence", "Live URL or GSC/rank evidence is present.", live_url)
    else:
        add(findings, stage, "NEEDS_EVIDENCE", "Observation evidence", "No live URL, GSC, or rank evidence was provided.")

    if contains_any(combined, [r"候補集合外", r"子KW認識", r"titleズレ", r"構造不足", r"内部リンク不足", r"信頼表示不足", r"SERP強度", r"時間要因", r"bottleneck", r"原因"]):
        add(findings, stage, "PASS", "Bottleneck classification", "Post-publish bottleneck classification is present.")
    else:
        add(findings, stage, "WARN", "Bottleneck classification", "Classify the issue before changing title or body.")

    query_spread_patterns = [r"exact target", r"親KW", r"子KW", r"child quer", r"parent quer", r"query spread", r"表示クエリ", r"完全一致"]
    if contains_any(combined, query_spread_patterns) or (target_query and target_query in combined and has_observation):
        add(findings, stage, "PASS", "Query-spread readout", "Exact target and child-query understanding is present or inferable.")
    else:
        add(findings, stage, "WARN", "Query-spread readout", "Record exact target query exposure and child-query exposure separately.")

    if contains_any(combined, [r"7日", r"14日", r"28日", r"7-day", r"14-day", r"28-day", r"1週", r"2週", r"4週", r"観測", r"定点"]):
        add(findings, stage, "PASS", "Observation cadence", "Observation cadence is present.")
    else:
        add(findings, stage, "WARN", "Observation cadence", "Add a 7/14/28-day or equivalent observation plan.")

    if contains_any(combined, [r"次アクション", r"next action", r"本文改稿", r"title変更", r"内部リンク", r"ハブ", r"カテゴリ", r"query変更", r"保留"]):
        add(findings, stage, "PASS", "Next action", "Next action is classified.")
    else:
        add(findings, stage, "WARN", "Next action", "State whether the next move is rewrite, title, internal links, hub, retarget, or wait.")


def render_report(args: argparse.Namespace, findings: list[Finding]) -> str:
    summary = status_summary(findings)
    overall = overall_status(findings)
    generated_at = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    inputs = [
        ("stage", args.stage),
        ("target_query", args.target_query or ""),
        ("article", str(args.article) if args.article else ""),
        ("research", ", ".join(str(path) for path in args.research)),
        ("package", str(args.package) if args.package else ""),
        ("live_url", args.live_url or ""),
        ("site_profile", str(args.site_profile) if args.site_profile else ""),
    ]

    lines = [
        "# SEO Article Check Report",
        "",
        f"- Generated: {generated_at}",
        f"- Overall: `{overall}`",
        "",
        "## Inputs",
        "",
    ]
    for key, value in inputs:
        lines.append(f"- {key}: {value or '(none)'}")

    lines += [
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status in ["FAIL", "NEEDS_EVIDENCE", "WARN", "PASS"]:
        lines.append(f"| {status} | {summary[status]} |")

    lines += ["", "## Findings", ""]
    for finding in findings:
        lines.append(f"### {finding.stage}: {finding.check}")
        lines.append("")
        lines.append(f"- Status: `{finding.status}`")
        lines.append(f"- Message: {finding.message}")
        if finding.evidence:
            lines.append(f"- Evidence: {finding.evidence}")
        lines.append("")

    lines += ["## Next Action Hints", ""]
    if summary["FAIL"]:
        lines.append("- Fix `FAIL` items before publishing or handing off.")
    if summary["NEEDS_EVIDENCE"]:
        lines.append("- Collect missing SERP, GSC, package, or live HTML evidence before making SEO decisions.")
    if summary["WARN"]:
        lines.append("- Either fix `WARN` items or record why the tradeoff is acceptable.")
    if overall == "PASS":
        lines.append("- No blocking issue was detected by the text-pattern CI. Human SERP and domain review still applies.")
    return "\n".join(lines).rstrip() + "\n"


def input_dict(args: argparse.Namespace) -> dict[str, str | list[str]]:
    return {
        "stage": args.stage,
        "target_query": args.target_query or "",
        "article": str(args.article) if args.article else "",
        "research": [str(path) for path in args.research],
        "package": str(args.package) if args.package else "",
        "live_url": args.live_url or "",
        "site_profile": str(args.site_profile) if args.site_profile else "",
    }


def render_json_report(args: argparse.Namespace, findings: list[Finding]) -> str:
    payload = {
        "generated": dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "overall": overall_status(findings),
        "summary": status_summary(findings),
        "inputs": input_dict(args),
        "findings": [finding.to_dict() for finding in findings],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_research_template(query: str) -> str:
    today = dt.date.today().isoformat()
    query_value = query or "<query>"
    return f"""# SERP Research: {query_value}

- Date: {today}
- Search source:
- Keyword-source feature:
- Source reference / export:
- Captured time:
- Source data time:
- Engine / country / language / device:
- Rank range:
- Features used / unavailable / skipped with reason:
- Google UI check reason (only if needed):
- Google URL:
- q: {query_value}
- start:
- hl / gl / pws:
- Chrome screen state / captured time:
- Location / personalization:
- Login/profile notes:
- Candidate volume / difficulty:

## SERP Features

- Ads:
- AI Overview:
- Featured snippet:
- PAA:
- Video pack:
- Image pack:
- Local/map:
- Other:

Organic rank exclusion notes:
- Ads / AI Overview / PAA / featured snippet / video or image pack:
- Sitelinks / duplicate URL fragments / same-article fragments:
- Other modules not counted as organic rank:

## Page Type Mix

- Articles:
- LP / service pages:
- Category / list pages:
- Q&A / forum:
- Official / company pages:
- Video / image-heavy pages:
- Other:
- Dominant winning page type:

## Organic Top 10

| Rank | URL | Page type | Title | H1 | Main H2/H3 | Immediate answer | CTA/path | Why this rank |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |  |

Unreadable or unconfirmed ranks:
- <rank>: <blocked / JS required / not fetched / snippet only / SERP module ambiguity>

## Rank Ladder: 10 -> 1

10 -> 6:
-

5 -> 3:
-

2 -> 1:
-

Why rank 1 looks like the representative answer:
-

## Title Top 10 Comparison

Use this section before deciding the article title.

| Rank | Title | Subject | Front-loaded words | Condition/anxiety/solution words | Naturalness | Intent fit | Use / avoid |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |

Title decision:
- Adopt:
- Avoid:
- Why our title can compete:

## Structure Top 10 Comparison

Use this section before deciding the outline.

| Rank | H1 / opening answer | H2/H3 order | Must-have sections | Examples / question blocks when present / media | CTA/path | Structural strength | What to copy or avoid |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |

Structure comparison notes:
- Top 1-3 common strengths:
- Top 6-10 weaknesses:
- Common must-have sections:
- Differentiators that should not replace must-have sections:

## Winning Structure Decision

- Final H2/H3 order:
- Depth by section:
- Opening answer:
- Question-block only if needed / table / image or gallery plan:
- Internal links / parent-child links:
- Service page or consultation CTA placement:
- Why this structure can beat similar lower pages:

## Top 10 -> Article Structure Rationale

Use this section to answer: after checking the top 10, why this outline?

| SERP evidence | Ranks/pages | Article section | Decision | Reason |
| --- | --- | --- | --- | --- |
|  |  |  | include / exclude / keep thin / split / internal-link out |  |
|  |  |  | include / exclude / keep thin / split / internal-link out |  |
|  |  |  | include / exclude / keep thin / split / internal-link out |  |
|  |  |  | include / exclude / keep thin / split / internal-link out |  |

Notes:
- Do not only list H2s. Tie each H2/H3 to observed top-10 patterns.
- If a top-10 topic is intentionally not covered deeply, explain whether it is being split to a child/sibling article or handled by an internal link.

## Lower-Page Comparison: 11 -> 20

| Rank | URL | Similarity to our article | Why it may be lower | What not to copy |
| ---: | --- | --- | --- | --- |
| 11 |  |  |  |  |
| 12 |  |  |  |  |
| 13 |  |  |  |  |
| 14 |  |  |  |  |
| 15 |  |  |  |  |
| 16 |  |  |  |  |
| 17 |  |  |  |  |
| 18 |  |  |  |  |
| 19 |  |  |  |  |
| 20 |  |  |  |  |

## Fallen-Page Comparison: 20 -> 30

Use this section to answer: why are similar pages not in the top 10?

| Rank | URL | Similarity to our article | Why it falls below top 10 | What not to copy |
| ---: | --- | --- | --- | --- |
| 20 |  |  |  |  |
| 21 |  |  |  |  |
| 22 |  |  |  |  |
| 23 |  |  |  |  |
| 24 |  |  |  |  |
| 25 |  |  |  |  |
| 26 |  |  |  |  |
| 27 |  |  |  |  |
| 28 |  |  |  |  |
| 29 |  |  |  |  |
| 30 |  |  |  |  |

## SERP Standard Answer

- What the SERP answers first:
- Common must-have sections:
- Common examples/templates:
- Common warnings/edge cases:
- Common CTA or next action:

## Parent / Child Topic Judgment

- Classification: parent / child / mixed / unknown
- Confidence: high / medium / low
- Evidence:
- SERP breadth:
- Rank ladder:
- Lower-page comparison:
- SERP features:
- Query variants that likely belong inside this page:
- Query variants that likely need separate pages:
- GSC query spread if published:
- Decision branch:
  - parent / child / mixed / unknown action:

## Intent-Fit Comparison

Current/planned article:
-

Mismatch risk:
-

Decision:
- write / rewrite existing URL / split / merge / retarget / defer

## Article Direction

- Title intent lock:
  - Main action word:
  - Anxiety word:
  - Condition word:
  - Solution word:
- Opening answer:
- H2/H3 structure decision:
- Internal links to add:
- Differentiation that does not replace must-have answers:

## Observation Plan

- First GSC check:
- 7-day check:
- 14-day check:
- 28-day check:
- Expected early signal:
"""


def should_exit_nonzero(overall: str, fail_on: str) -> bool:
    threshold = FAIL_ON_STATUS[fail_on]
    return STATUS_ORDER[overall] >= STATUS_ORDER[threshold]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run warning-centered SEO checks for article artifacts.")
    parser.add_argument("--article", type=Path, help="Article markdown or HTML path.")
    parser.add_argument("--research", type=Path, action="append", default=[], help="SERP/GSC/research markdown path. May be repeated.")
    parser.add_argument("--package", type=Path, help="WordPress/package HTML or markdown path.")
    parser.add_argument("--target-query", default="", help="Primary target query.")
    parser.add_argument("--live-url", default="", help="Published URL, if available.")
    parser.add_argument("--site-profile", type=Path, help="Optional JSON/YAML project profile path for simple overrides such as title_max_chars.")
    parser.add_argument("--stage", choices=["all", "prepublish", "research", "draft", "package", "post_publish"], default="prepublish")
    parser.add_argument("--output", type=Path, default=Path("blog-agent-seo-check-report.md"), help="Markdown report output path.")
    parser.add_argument("--json-output", type=Path, help="Optional structured JSON report output path.")
    parser.add_argument("--fail-on", choices=["fail", "needs_evidence", "warn"], default="fail", help="Choose which overall status exits non-zero.")
    parser.add_argument("--write-research-template", type=Path, help="Write a SERP research template and exit if no article/research/package input is provided.")
    parser.add_argument("--stdout-only", action="store_true", help="Print report without writing --output.")
    return parser.parse_args(argv)


def validate_paths(paths: Iterable[Path | None]) -> list[str]:
    errors = []
    for path in paths:
        if path and not path.exists():
            errors.append(f"Missing input file: {path}")
    return errors


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.write_research_template:
        args.write_research_template.parent.mkdir(parents=True, exist_ok=True)
        args.write_research_template.write_text(render_research_template(args.target_query), encoding="utf-8")
        print(f"Research template: {args.write_research_template}")
        if not (args.article or args.research or args.package or args.live_url):
            return 0

    errors = validate_paths([args.article, args.package, args.site_profile, *args.research])
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 2

    article_text = read_text(args.article)
    research_texts = [read_text(path) for path in args.research]
    package_text = read_text(args.package)
    site_profile = load_site_profile(args.site_profile)
    findings: list[Finding] = []
    enabled_stages = {"research", "draft", "package"} if args.stage == "prepublish" else {args.stage}
    if args.stage == "all":
        enabled_stages = {"research", "draft", "package", "post_publish"}

    if "research" in enabled_stages:
        research_ci(findings, research_texts, args.target_query)
    if "draft" in enabled_stages:
        draft_ci(findings, article_text, bool("".join(research_texts).strip()), args.target_query, site_profile)
    if "package" in enabled_stages:
        package_ci(findings, package_text, args.package)
    if "post_publish" in enabled_stages:
        post_publish_ci(findings, research_texts, args.live_url, args.target_query)

    report = render_report(args, findings)
    if not args.stdout_only:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(render_json_report(args, findings), encoding="utf-8")

    summary = status_summary(findings)
    print(f"Overall: {overall_status(findings)}")
    print("Counts: " + ", ".join(f"{status}={summary[status]}" for status in ["FAIL", "NEEDS_EVIDENCE", "WARN", "PASS"]))
    if args.stdout_only:
        print()
        print(report)
    else:
        print(f"Report: {args.output}")
        if args.json_output:
            print(f"JSON: {args.json_output}")
    return 1 if should_exit_nonzero(overall_status(findings), args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
