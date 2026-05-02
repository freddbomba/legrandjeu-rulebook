#!/usr/bin/env python3
"""Assemble book.html from chapter fragments.

Usage:  python3 build-book.py

Reads ch*.html fragments in order and wraps them in the HTML shell.
"""
from pathlib import Path

HERE = Path(__file__).parent

CHAPTERS = [
    "ch00-front.html",
    "ch01-about.html",
    "ch02-permacoin.html",
    "ch03-pandemic.html",
    "ch04-downunder.html",
    "ch05-sou.html",
    "ch06-messina.html",
    "ch99-appendix.html",
]

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Le Grand Jeu — Scenarios</title>
<link rel="stylesheet" href="book.css">
</head>
<body>

{body}

</body>
</html>
"""

def main():
    parts = []
    for name in CHAPTERS:
        path = HERE / name
        if not path.exists():
            print(f"  ! missing: {name}")
            continue
        parts.append(path.read_text())
        print(f"  + {name}")
    out = SHELL.format(body="\n\n".join(parts))
    (HERE / "book.html").write_text(out)
    print(f"\nWrote book.html ({len(out):,} chars)")

if __name__ == "__main__":
    main()
