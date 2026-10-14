"""Build a usable HTML preview of the Quarto sources with system Pandoc.

`quarto render` remains the canonical rebuild command. This fallback is used
only when the Quarto CLI is not available in the execution environment.
"""
from __future__ import annotations

import html
import re
import shutil
import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
NAV = [
    ("index.html", "Overview"),
    ("slides.html", "Day 1 slides"),
    ("reference.html", "Pattern guide"),
]


def source(name: str) -> tuple[dict, str]:
    raw = (ROOT / f"{name}.qmd").read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if match is None:
        raise ValueError(f"Missing YAML front matter in {name}.qmd")
    return yaml.safe_load(match.group(1)), raw[match.end():]


def pandoc(markdown: str) -> str:
    proc = subprocess.run(
        ["pandoc", "--from=markdown+fenced_divs", "--to=html5"],
        input=markdown,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout


def head(title: str, stylesheet: str) -> str:
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)}</title>'
        f'<link rel="stylesheet" href="{stylesheet}"></head>'
    )


def page(name: str) -> None:
    meta, markdown = source(name)
    title = meta["title"]
    nav_parts = []
    for href, label in NAV:
        active = ' aria-current="page"' if href == name + ".html" else ""
        nav_parts.append(f'<a href="{href}"{active}>{label}</a>')
    nav = "".join(nav_parts)
    subtitle = meta.get("subtitle", "")
    body = (
        head(title, "assets/site.css")
        + f'<body><nav class="site-nav"><strong>STAT 386 · Regex</strong>{nav}</nav>'
        + f'<main><h1>{html.escape(title)}</h1>'
        + (f'<p class="site-subtitle">{html.escape(subtitle)}</p>' if subtitle else "")
        + pandoc(markdown)
        + '</main><footer class="site-footer">STAT 386 · Regular expressions for data wrangling</footer></body></html>'
    )
    (OUT / f"{name}.html").write_text(body, encoding="utf-8")


def slides() -> None:
    meta, markdown = source("slides")
    chunks = re.split(r"(?m)^## ", markdown)
    sections = [
        f'<section class="active" aria-label="Title slide"><h1>{html.escape(meta["title"])}</h1>'
        f'<p class="site-subtitle">{html.escape(meta["subtitle"])}</p>'
        '<p>STAT 386 · Data wrangling</p></section>'
    ]
    for chunk in chunks[1:]:
        sections.append('<section>' + pandoc('## ' + chunk) + '</section>')
    js = '''<script>
    const slides = [...document.querySelectorAll('.deck section')];
    const counter = document.querySelector('#slide-counter');
    const previous = document.querySelector('#previous');
    const next = document.querySelector('#next');
    let current = 0;
    function show(index) {
      current = Math.max(0, Math.min(slides.length - 1, index));
      slides.forEach((slide, i) => slide.classList.toggle('active', i === current));
      counter.textContent = `${current + 1} / ${slides.length}`;
      previous.disabled = current === 0;
      next.disabled = current === slides.length - 1;
      history.replaceState(null, '', '#slide-' + (current + 1));
    }
    previous.addEventListener('click', () => show(current - 1));
    next.addEventListener('click', () => show(current + 1));
    document.addEventListener('keydown', (event) => {
      if (['ArrowRight', 'PageDown', ' '].includes(event.key)) { event.preventDefault(); show(current + 1); }
      if (['ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); show(current - 1); }
    });
    const start = Number(location.hash.match(/^#slide-(\\d+)$/)?.[1]);
    show(Number.isFinite(start) && start > 0 ? start - 1 : 0);
    </script>'''
    output = (
        head(meta["title"], "assets/slides.css")
        + '<body class="deck-page"><div class="deck-shell">'
        + '<header class="deck-topbar"><a href="index.html">← Lecture home</a>'
        + '<span class="spacer"></span><span>Day 1 · Reading and building patterns</span></header>'
        + '<main class="deck" aria-label="Lecture slides">'
        + '\n'.join(sections)
        + '</main><nav class="deck-controls" aria-label="Slide navigation">'
        + '<button type="button" id="previous" aria-label="Previous slide">Previous</button>'
        + '<span id="slide-counter"></span>'
        + '<button type="button" id="next" aria-label="Next slide">Next</button></nav>'
        + '</div>' + js + '</body></html>'
    )
    (OUT / "slides.html").write_text(output, encoding="utf-8")
    print(f"Built {len(sections)} slides")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    assets = OUT / "assets"
    assets.mkdir(exist_ok=True)
    for name in ["site.css", "slides.css"]:
        shutil.copy2(ROOT / "styles" / name, assets / name)
    for directory, names in {
        "data": ["talks_sample.csv"],
        "notebooks": ["regex_follow_along.ipynb", "regex_practice.ipynb"],
    }.items():
        target = OUT / directory
        target.mkdir(exist_ok=True)
        for name in names:
            shutil.copy2(ROOT / directory / name, target / name)
    for name in ["index", "reference"]:
        page(name)
    slides()
    (OUT / "follow-along.html").unlink(missing_ok=True)
    (OUT / ".nojekyll").touch()


if __name__ == "__main__":
    main()
