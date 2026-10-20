#!/usr/bin/env python3
"""Warn about repetitive structure and risky claims in Chinese long-form drafts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CONTRAST_PATTERNS = {
    "不是A而是B": re.compile(r"不是[^。！？\n]{1,45}(?:，)?而是"),
    "值得X的是": re.compile(r"(?:最)?值得[^。！？\n]{0,12}的是"),
    "之所以重要": re.compile(r"之所以重要"),
    "这意味着": re.compile(r"这意味着"),
}
OPENING_CONNECTORS = ("与此同时", "因此", "不过", "在此之后", "由此", "所以", "这也", "换句话说")
ABSTRACT_TERMS = ("信号", "转向", "范式", "约束", "维度", "层面", "路径", "机制")
CAUSAL_MARKERS = ("因为", "导致", "促使", "倒逼", "催生", "源于", "所以", "因此")
ATTRIBUTION_MARKERS = ("访谈", "报告", "官方", "提到", "表示", "认为", "称")
INFERENCE_MARKERS = ("可能", "更像", "表明", "说明", "意味着", "我的判断", "还不能证明")
TAKEAWAY_OPENERS = ("这", "因此", "所以", "由此", "表面上", "归根结底")
SENTENCE_RE = re.compile(r"[^。！？!?]+[。！？!?]?")
NUMBER_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?")


def strip_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"!\[[^]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    return re.sub(r"[*_`>#]", "", text).strip()


def sentence_count(paragraph: str) -> int:
    return sum(bool(item.strip()) for item in SENTENCE_RE.findall(paragraph))


def parse_sections(text: str) -> list[dict]:
    sections: list[dict] = []
    current = {"heading": "导语", "paragraphs": []}
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        if re.match(r"^##\s+", block):
            if current["paragraphs"]:
                sections.append(current)
            current = {"heading": re.sub(r"^##\s+", "", block), "paragraphs": []}
        elif not block.startswith("#") and not block.startswith("---"):
            cleaned = strip_markdown(block)
            if cleaned:
                current["paragraphs"].append(cleaned)
    if current["paragraphs"]:
        sections.append(current)
    return sections


def audit(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    sections = parse_sections(text)
    paragraphs = [p for section in sections for p in section["paragraphs"]]
    counts = [sentence_count(p) for p in paragraphs]
    lengths = [sum(len(p) for p in section["paragraphs"]) for section in sections]
    patterns = {label: len(pattern.findall(text)) for label, pattern in CONTRAST_PATTERNS.items()}
    connectors = [p for p in paragraphs if p.startswith(OPENING_CONNECTORS)]
    abstract = {term: text.count(term) for term in ABSTRACT_TERMS if text.count(term)}
    number_dense = [p[:180] for p in paragraphs if len(NUMBER_RE.findall(p)) >= 3]
    causal = [p[:180] for p in paragraphs if any(marker in p for marker in CAUSAL_MARKERS)]
    mixed = [
        p[:180]
        for p in paragraphs
        if any(marker in p for marker in ATTRIBUTION_MARKERS)
        and any(marker in p for marker in INFERENCE_MARKERS)
    ]
    endings = []
    for section in sections:
        if section["paragraphs"]:
            final = section["paragraphs"][-1]
            if final.startswith(TAKEAWAY_OPENERS) and len(final) <= 120:
                endings.append({"section": section["heading"], "ending": final[:120]})

    warnings = []
    mean = sum(lengths) / len(lengths) if lengths else 0
    near_mean = sum(abs(n - mean) <= mean * 0.15 for n in lengths) if mean else 0
    if patterns["不是A而是B"] > 2:
        warnings.append("‘不是 A，而是 B’超过 2 次。")
    if patterns["值得X的是"]:
        warnings.append("出现‘值得 X 的是’，检查能否直接进入事实。")
    if paragraphs and len(connectors) / len(paragraphs) > 0.18:
        warnings.append("超过 18% 的段落以常见连接词开头。")
    if len(lengths) >= 4 and near_mean / len(lengths) >= 0.6:
        warnings.append("多数章节长度接近平均值，检查是否平均用力。")
    if counts and sum(n == 1 for n in counts) / len(counts) < 0.08:
        warnings.append("单句转折段偏少。")
    if counts and sum(n >= 4 for n in counts) / len(counts) < 0.08:
        warnings.append("深解释段偏少，检查是否切得过碎。")
    if len(endings) >= 2:
        warnings.append("多个章节以短总结句收尾。")
    plain_chars = len(strip_markdown(text))
    if plain_chars and sum(abstract.values()) / plain_chars * 1000 >= 2:
        warnings.append("抽象审计词超过每千字 2 次。")
    if number_dense:
        warnings.append(f"{len(number_dense)} 个段落包含至少 3 个数字。")
    if causal:
        warnings.append(f"{len(causal)} 个段落包含因果标记，需核对来源或机制。")
    if mixed:
        warnings.append(f"{len(mixed)} 个段落同时出现来源归属与推论词。")

    return {
        "file": str(path.resolve()),
        "sections": [
            {"heading": section["heading"], "characters": lengths[i], "paragraphs": len(section["paragraphs"])}
            for i, section in enumerate(sections)
        ],
        "formula_counts": patterns,
        "paragraph_opening_connectors": len(connectors),
        "abstract_term_counts": abstract,
        "number_dense_paragraphs": number_dense,
        "causal_claims_for_review": causal,
        "attribution_inference_review": mixed,
        "possible_takeaway_endings": endings,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="Markdown or text draft to audit")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()
    result = audit(args.draft)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"File: {result['file']}")
    for section in result["sections"]:
        print(f"- {section['heading']}: {section['characters']} chars, {section['paragraphs']} paragraphs")
    print(f"Formula counts: {result['formula_counts']}")
    print(f"Paragraph-opening connectors: {result['paragraph_opening_connectors']}")
    print(f"Abstract terms: {result['abstract_term_counts']}")
    print("Warnings:")
    for warning in result["warnings"] or ["none; still review in context"]:
        print(f"- {warning}")


if __name__ == "__main__":
    main()
