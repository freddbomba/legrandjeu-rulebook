#!/usr/bin/env python3
"""Convert Book 2 markdown chapters to HTML fragments matching book.css.

Usage:  python3 convert-md.py [ch08-norway.md ...]
        python3 convert-md.py            # converts all ch*.md in cwd

Each .md file produces a same-named .html fragment.
These fragments are meant to be assembled by build-book.py.

Design notes
────────────
The CSS in book.css defines a very specific HTML structure:
  <section class="chapter" data-title="Norway">
    <div class="chapter-opener">
      <p class="ch-num">Chapter VIII</p>
      <h1>Norway — Oslo</h1>
      <dl class="ch-meta"> ... </dl>
    </div>
    <h2 class="section">...</h2>
    <p>...</p>
    <div class="pull">...</div>
    ...
    <p class="chapter-end">· · ·</p>
  </section>

This script parses each markdown file's YAML front matter for metadata
(chapter number, title, short_title) and converts the body line-by-line,
mapping markdown constructs to the HTML classes above.
"""

import re
import sys
import yaml
from pathlib import Path

# Matches [IMAGE: filename — caption text]  (em-dash or double-hyphen separator)
IMAGE_RE = re.compile(r'^\[IMAGE:\s*(.+?)\s*(?:—|--)\s*(.*?)\]$')


# ── Inline formatting ────────────────────────────────────────────────

def inline(text):
    """Convert inline markdown (bold, italic) to HTML.

    Order matters: bold (**) before italic (*) so we don't eat the
    double-asterisks piecemeal.
    """
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


# ── Front matter ─────────────────────────────────────────────────────

def split_front_matter(text):
    """Return (yaml_dict, body_string).  Tolerates missing front matter."""
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}, parts[2].strip()
    return {}, text.strip()


# ── Metadata table ───────────────────────────────────────────────────

def parse_meta_table(lines, start):
    """Parse a pipe-delimited markdown table into (key, value) pairs.

    Returns (pairs_list, index_after_table).
    Skips the |---|---| separator line automatically.
    """
    pairs = []
    i = start
    while i < len(lines) and lines[i].strip().startswith('|'):
        row = lines[i].strip()
        # Skip separator rows like |---|---|
        if re.match(r'^\|[\s\-:|]+\|$', row):
            i += 1
            continue
        cells = [c.strip() for c in row.split('|')]
        # split('|') gives ['', cell1, cell2, ''] for |cell1|cell2|
        cells = [c for c in cells if c]
        if len(cells) >= 2:
            key = re.sub(r'\*\*(.+?)\*\*', r'\1', cells[0]).strip()
            val = inline(cells[1].strip())
            if key and val:
                pairs.append((key, val))
        i += 1
    return pairs, i


# ── Blockquote → pull-quote ──────────────────────────────────────────

def render_pull_quote(raw_lines):
    """Convert collected blockquote lines to a .pull div.

    The Book 2 convention for bilingual quotes is:
        > *"Norwegian text"*
        >
        > "English translation"

    We render the first non-empty line as the main quote text and
    subsequent lines as .pull-attr (which the CSS styles in normal
    weight, smaller type — ideal for translations).
    """
    # Strip blockquote markers and blank lines
    content = []
    for rl in raw_lines:
        text = rl.strip()
        if text:
            content.append(inline(text))

    if not content:
        return ''

    parts = ['<div class="pull">']
    parts.append(content[0])
    for extra in content[1:]:
        parts.append(f'<span class="pull-attr">{extra}</span>')
    parts.append('</div>')
    return '\n'.join(parts)


# ── Main converter ───────────────────────────────────────────────────

def convert(md_text):
    """Convert one chapter's markdown to an HTML fragment string."""

    meta, body = split_front_matter(md_text)
    ch_num   = meta.get('chapter', '')
    title    = meta.get('title', '')
    short    = meta.get('short_title', title)

    lines = body.split('\n')
    out   = []           # accumulated HTML lines
    buf   = []           # paragraph accumulator
    qbuf  = []           # blockquote accumulator
    lbuf  = []           # list-item accumulator
    in_bq = False
    in_li = False
    opener_closed = False

    # ── helpers ──

    def flush_para():
        """Emit any buffered paragraph lines as a <p>."""
        nonlocal buf
        if buf:
            text = ' '.join(buf)
            out.append(f'<p>{inline(text)}</p>')
            buf = []

    def flush_quote():
        """Emit any buffered blockquote lines as a .pull div."""
        nonlocal in_bq, qbuf
        if qbuf:
            out.append(render_pull_quote(qbuf))
            qbuf = []
        in_bq = False

    def flush_list():
        """Emit any buffered list items as a <ul>."""
        nonlocal in_li, lbuf
        if lbuf:
            out.append('<ul>')
            for item in lbuf:
                out.append(f'  <li>{item}</li>')
            out.append('</ul>')
            lbuf = []
        in_li = False

    def ensure_opener_closed():
        """Close the chapter-opener div if still open."""
        nonlocal opener_closed
        if not opener_closed:
            out.append('</div><!-- /chapter-opener -->')
            opener_closed = True

    # ── line-by-line pass ──

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── H1: chapter title (first one only) ──
        if stripped.startswith('# ') and not any('class="chapter"' in o for o in out):
            flush_para()
            h1_text = stripped[2:]

            # Use YAML title for h1 (avoids duplicating "Chapter VIII"
            # which already appears in .ch-num)
            display_title = title if title else h1_text

            # id="ch-VIII" etc. for TOC anchor links
            ch_id = f' id="ch-{ch_num}"' if ch_num else ''
            out.append(f'<section class="chapter"{ch_id} data-title="{short}">')
            out.append('<div class="chapter-opener">')
            if ch_num:
                out.append(f'<p class="ch-num">Chapter {ch_num}</p>')
            out.append(f'<h1>{display_title}</h1>')

            # Look ahead: is the next non-blank line a table?
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines) and lines[j].strip().startswith('|'):
                pairs, j = parse_meta_table(lines, j)
                if pairs:
                    out.append('<dl class="ch-meta">')
                    for k, v in pairs:
                        out.append(f'  <dt>{k}</dt>')
                        out.append(f'  <dd>{v}</dd>')
                    out.append('</dl>')
                i = j
                out.append('</div><!-- /chapter-opener -->')
                opener_closed = True
                continue
            else:
                out.append('</div><!-- /chapter-opener -->')
                opener_closed = True
                i += 1
                continue

        # ── H2: section heading ──
        if stripped.startswith('## '):
            flush_para()
            flush_quote()
            flush_list()
            ensure_opener_closed()
            heading = inline(stripped[3:])
            out.append(f'\n<h2 class="section">{heading}</h2>')
            i += 1
            continue

        # ── H3: subsection heading ──
        if stripped.startswith('### '):
            flush_para()
            flush_quote()
            flush_list()
            ensure_opener_closed()
            heading = inline(stripped[4:])
            out.append(f'\n<h3>{heading}</h3>')
            i += 1
            continue

        # ── Blockquote lines ──
        if stripped.startswith('> '):
            flush_para()
            flush_list()
            ensure_opener_closed()
            in_bq = True
            # Strip the '> ' prefix
            qbuf.append(stripped[2:])
            i += 1
            continue

        if stripped == '>' and in_bq:
            # Empty continuation line inside a blockquote — skip
            i += 1
            continue

        # ── End of blockquote (non-> line after blockquote) ──
        if in_bq:
            flush_quote()
            # Fall through to process this line normally

        # ── Image placeholder [IMAGE: file — caption] ──
        img_match = IMAGE_RE.match(stripped)
        if img_match:
            flush_para()
            flush_list()
            ensure_opener_closed()
            filename = img_match.group(1).strip()
            raw_caption = img_match.group(2).strip()
            caption_html = inline(raw_caption)
            caption_plain = re.sub(r'<[^>]+>', '', caption_html)
            out.append('<figure>')
            out.append(f'  <img src="assets/spes/{filename}" alt="{caption_plain}">')
            out.append(f'  <figcaption>{caption_html}</figcaption>')
            out.append('</figure>')
            i += 1
            continue

        # ── Unordered list item ──
        if stripped.startswith('- ') or stripped.startswith('* '):
            flush_para()
            ensure_opener_closed()
            in_li = True
            lbuf.append(inline(stripped[2:]))
            i += 1
            continue

        # ── End of list (non-list line after list items) ──
        if in_li:
            flush_list()
            # Fall through to process this line normally

        # ── Blank line ──
        if stripped == '':
            flush_para()
            flush_list()
            i += 1
            continue

        # ── Table row outside the opener (shouldn't happen often) ──
        if stripped.startswith('|'):
            flush_para()
            i += 1
            continue

        # ── Regular paragraph text ──
        ensure_opener_closed()
        buf.append(stripped)
        i += 1

    # ── Flush anything remaining ──
    flush_para()
    flush_quote()
    flush_list()
    ensure_opener_closed()

    out.append('\n<p class="chapter-end">· · ·</p>')
    out.append('</section>')

    return '\n'.join(out)


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    cwd = Path('.')

    if len(sys.argv) > 1:
        files = [Path(a) for a in sys.argv[1:]]
    else:
        files = sorted(cwd.glob('ch*.md'))

    # Skip ch00-front.md — its HTML is hand-crafted, not auto-converted
    files = [f for f in files if f.name != 'ch00-front.md']

    if not files:
        print("No ch*.md files found.")
        sys.exit(1)

    for md_path in files:
        html = convert(md_path.read_text(encoding='utf-8'))
        out_path = md_path.with_suffix('.html')
        out_path.write_text(html, encoding='utf-8')
        print(f"  {md_path.name}  →  {out_path.name}")

    print(f"\nConverted {len(files)} file(s).")


if __name__ == '__main__':
    main()
