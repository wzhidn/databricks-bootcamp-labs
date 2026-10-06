#!/usr/bin/env python3
"""Generate the participant branches from the annotated sources (instructor tool).

Markers
-------
* Block:  a line containing ``SOLUTION-BEGIN lab-NN: <hint>`` … a line containing ``SOLUTION-END``.
          Kept when building level >= NN, otherwise replaced by ``<prefix>TODO (lab-NN): <hint>``
          where <prefix> is whatever precedes the marker on its line (e.g. ``# MAGIC -- ``).
* File:   ``SOLUTION-FILE lab-NN`` in the first 3 lines. The file is omitted below level NN.

Usage
-----
    python tools/build_checkpoints.py <source_dir> <out_dir> <level>
level: 0 = starter (main), 1..6 = checkpoint after lab NN, 99 = full solution.
"""
from __future__ import annotations

import os
import re
import shutil
import sys

BEGIN = re.compile(r"^(?P<prefix>.*?)SOLUTION-BEGIN lab-(?P<lab>\d+):\s*(?P<hint>.*)$")
END = re.compile(r"SOLUTION-END")
FILE = re.compile(r"SOLUTION-FILE lab-(?P<lab>\d+)")

SKIP_DIRS = {".git", "tools", "_old", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".databricks"}
SKIP_FILES = {"INSTRUCTOR.md"}
TEXT_EXT = {".py", ".sql", ".yml", ".yaml", ".md", ".toml", ".txt", ".json", ""}

# Copies that activate CI in the lab 06 checkpoint and the solution branch.
CI_COPIES = {   # activated from the DevOps lab (lab 06) onwards
    "labs/lab-06-devops/github/bundle-cicd.yml": ".github/workflows/bundle-cicd.yml",
    "labs/lab-06-devops/github/bundle-rollback.yml": ".github/workflows/bundle-rollback.yml",
    "labs/lab-06-devops/azure-devops/azure-pipelines.yml": ".azure-pipelines/azure-pipelines.yml",
    "labs/lab-06-devops/azure-devops/azure-pipelines-rollback.yml": ".azure-pipelines/azure-pipelines-rollback.yml",
    "labs/lab-06-devops/azure-devops/templates/install-databricks-cli.yml":
        ".azure-pipelines/templates/install-databricks-cli.yml",
}


def transform(text: str, level: int) -> str | None:
    lines = text.splitlines(keepends=True)
    for line in lines[:3]:
        m = FILE.search(line)
        if m:
            if level < int(m.group("lab")):
                return None
            lines = [ln for ln in lines if not FILE.search(ln)]
            break
    out, i = [], 0
    while i < len(lines):
        m = BEGIN.match(lines[i].rstrip("\n"))
        if not m:
            out.append(lines[i])
            i += 1
            continue
        j = i + 1
        while j < len(lines) and not END.search(lines[j]):
            j += 1
        if j == len(lines):
            raise ValueError(f"Unterminated SOLUTION-BEGIN at line {i + 1}")
        if level >= int(m.group("lab")):
            out.extend(lines[i + 1:j])
        else:
            out.append(f"{m.group('prefix')}TODO (lab-{m.group('lab')}): {m.group('hint')}\n")
        i = j + 1
    return "".join(out)


def build(src: str, dst: str, level: int) -> None:
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in SKIP_FILES:
                continue
            s = os.path.join(root, name)
            rel = os.path.relpath(s, src)
            d = os.path.join(dst, rel)
            if os.path.splitext(name)[1] in TEXT_EXT:
                result = transform(open(s, encoding="utf-8").read(), level)
                if result is None:
                    continue
                os.makedirs(os.path.dirname(d), exist_ok=True)
                with open(d, "w", encoding="utf-8") as fh:
                    fh.write(result)
            else:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
    if level >= 6:
        for s, d in CI_COPIES.items():
            os.makedirs(os.path.dirname(os.path.join(dst, d)), exist_ok=True)
            shutil.copy2(os.path.join(dst, s), os.path.join(dst, d))


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], int(sys.argv[3]))
