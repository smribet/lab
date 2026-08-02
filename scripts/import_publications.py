"""Convert the CV's LaTeX publication list into MyST Markdown."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


def clean_latex(value: str) -> str:
    value = re.sub(
        r"\\href\{([^{}]+)\}\{\\textit\{([^{}]+)\}\}",
        r"[*\2*](\1)",
        value,
    )
    value = re.sub(r"\\textit\{([^{}]+)\}", r"*\1*", value)
    value = re.sub(r"\$_\{([^{}]+)\}\$", r"<sub>\1</sub>", value)
    value = re.sub(r"\$_([^$])\$", r"<sub>\1</sub>", value)
    value = value.replace(r"\thinspace", "")
    value = value.replace(r"\&", "&")
    value = value.replace("``", '“').replace("''", '”')
    value = re.sub(r'"([^"]+)"', r'“\1”', value)
    value = value.replace("“ ", "“").replace(" ”", "”")
    value = value.replace(" -- ", " — ")
    value = value.replace("http://doi.org/", "https://doi.org/")
    # Crossref currently returns malformed metadata for this valid DOI, which
    # makes MyST's strict DOI transform fail. Link to the publisher instead.
    value = value.replace(
        "https://doi.org/10.1093/mam/ozaf059",
        "https://academic.oup.com/mam/article/31/4/ozaf059/8222547",
    )
    value = re.sub(r"\[(in press|featured article|invited review)\]", r"(*\1*)", value)
    value = value.replace("S.M. Ribet", "S. M. Ribet")
    value = value.replace("V.P. Dravid", "V. P. Dravid")
    return re.sub(r"\s+", " ", value).strip()


def parse(source: str) -> list[tuple[int, str, str]]:
    category = "publication"
    records: list[tuple[int, str, str]] = []
    current: list[str] = []

    def finish() -> None:
        if not current:
            return
        entry = clean_latex(" ".join(current))
        years = re.findall(r"\b20\d{2}\b", entry)
        if not years:
            raise ValueError(f"No year found for entry: {entry}")
        records.append((int(years[-1]), category, entry))
        current.clear()

    for raw_line in source.splitlines():
        line = raw_line.strip()
        if "Pre-prints" in line:
            finish()
            category = "preprint"
            continue
        if "Peer-reviewed" in line:
            finish()
            category = "publication"
            continue
        if r"\begin{rSection}{Patents" in line:
            finish()
            category = "patent"
            continue
        if line.startswith(r"\item[]"):
            continue
        if line.startswith(r"\item "):
            finish()
            current.append(line[len(r"\item ") :])
        elif current and line and not line.startswith((r"\goodbreak", r"\vspace", r"\end{")):
            current.append(line)
    finish()
    return records


def render(records: list[tuple[int, str, str]]) -> str:
    by_year: dict[int, list[tuple[str, str]]] = defaultdict(list)
    for year, category, entry in records:
        by_year[year].append((category, entry))

    lines = [
        "---",
        "title: Publications",
        "---",
        "",
        "# Publications",
        "",
        "[View this publication record on Google Scholar](https://scholar.google.com/citations?user=g2-jjNwAAAAJ&hl=en&oi=ao).",
        "",
        "An asterisk (*) denotes equal contribution.",
    ]
    number = 1
    for year in sorted(by_year, reverse=True):
        lines.extend(("", f"## {year}", ""))
        for _, entry in by_year[year]:
            lines.append(f"{number}. {entry}")
            number += 1
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: import_publications.py INPUT.txt OUTPUT.md")
    source = Path(sys.argv[1]).read_text()
    records = parse(source)
    Path(sys.argv[2]).write_text(render(records))
    counts = defaultdict(int)
    for _, category, _ in records:
        counts[category] += 1
    print(f"wrote {len(records)} entries: {dict(counts)}")


if __name__ == "__main__":
    main()
