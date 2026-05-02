#!/usr/bin/env python3
"""Assemble book.html from chapter fragments — Book 2.

Usage:  python3 build-book.py

Finds all ch*.html fragments in the same directory, sorts them
by filename (so ch00 < ch01 < … < ch99), and wraps them in the
HTML shell.

Requires: convert-md.py to have been run first.
"""
from pathlib import Path

HERE = Path(__file__).parent

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Le Grand Jeu — Experiments in Playing the Small Game</title>
<link rel="stylesheet" href="book.css">
</head>
<body>

{body}

</body>
</html>
"""

def main():
    # Auto-detect all ch*.html files, sorted alphabetically
    chapters = sorted(HERE.glob("ch*.html"))

    if not chapters:
        print("No ch*.html files found. Run convert-md.py first.")
        return

    parts = []
    for path in chapters:
        parts.append(path.read_text(encoding="utf-8"))
        print(f"  + {path.name}")

    out = SHELL.format(body="\n\n".join(parts))
    (HERE / "book.html").write_text(out, encoding="utf-8")
    print(f"\nWrote book.html ({len(out):,} chars)")

if __name__ == "__main__":
    main()
