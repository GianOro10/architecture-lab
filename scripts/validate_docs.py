#!/usr/bin/env python3
"""Validate basic quality rules for Markdown documentation."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
errors = []
checked = 0

for path in sorted(ROOT.rglob("*.md")):
    if ".git" in path.parts:
        continue
    checked += 1
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT)

    if not text.strip():
        errors.append(f"{relative}: file is empty")
        continue

    if not text.lstrip().startswith("# "):
        errors.append(f"{relative}: missing top-level heading")

    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split()[0].strip("<>")
        if (
            not target
            or target.startswith(("#", "http://", "https://", "mailto:"))
        ):
            continue
        local_target = target.split("#", 1)[0]
        resolved = (path.parent / local_target).resolve()
        if not resolved.exists():
            errors.append(f"{relative}: missing local link target {local_target}")

if errors:
    print("\n".join(f"ERROR: {item}" for item in errors))
    sys.exit(1)

print(f"Validated {checked} Markdown files.")
