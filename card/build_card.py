"""Builds dark_mode.svg and light_mode.svg: ASCII portrait + neofetch-style info panel."""
import datetime as dt
from pathlib import Path
from xml.sax.saxutils import escape

USER = "DonDurkheim"
BORN = dt.date(2008, 9, 8)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

FONT_SIZE = 13
LINE_H = 16
CHAR_W = 7.8  # widest likely monospace fallback at 13px (Menlo, Courier)
ART_CHAR_W = 7.3  # portrait column budget; GAP absorbs wider fonts
PAD = 24
GAP = 36
INFO_W = 60  # characters per info line

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", ascii="#c9d1d9", key="#ffa657",
                 val="#a5d6ff", dots="#6e7681", head="#f0f6fc"),
    "light": dict(bg="#ffffff", border="#d0d7de", ascii="#24292f", key="#953800",
                  val="#0a3069", dots="#8c959f", head="#1f2328"),
}


def uptime(today):
    y, m, d = today.year - BORN.year, today.month - BORN.month, today.day - BORN.day
    if d < 0:
        m -= 1
        d += (today.replace(day=1) - dt.timedelta(days=1)).day
    if m < 0:
        y -= 1
        m += 12
    unit = lambda n, w: f"{n} {w}{'' if n == 1 else 's'}"
    return f"{unit(y, 'year')}, {unit(m, 'month')}, {unit(d, 'day')}"


# Everything under "Building @ Entelon" is sourced from entelon.co and dondurkheim.com.
def rows(today):
    return [
        ("title", "don@durkheim"),
        ("rule",),
        ("kv", "Role", "Co-founder & President, Entelon"),
        ("kv", "Kernel", "AI Research Engineer"),
        ("kv", "Uptime", uptime(today)),
        ("kv", "Host", "Kigali, Rwanda"),
        ("kv", "School", "Rwanda Coding Academy"),
        ("kv", "Robotics", "Ladybug FRC 9647, Software Lead"),
        ("blank",),
        ("kv", "Languages", "Python, TypeScript, Rust, C++, Java"),
        ("kv", "AI.ML", "PyTorch, LLM fine-tuning, ASR, TTS"),
        ("kv", "Backend", "FastAPI, Django, Node.js, Postgres"),
        ("kv", "Frontend", "React, Next.js, SwiftUI"),
        ("blank",),
        ("sec", "Building @ Entelon"),
        ("kv", "Kinyarwanda.TTS", "VITS on ~500h of audio"),
        ("kv", "Kinyarwanda.LLM", "co-developing"),
        ("kv", "Mamora AI", "community wellbeing platform"),
        ("kv", "Visko", "paperless field research"),
        ("kv", "Klok AI", "AI-assisted exam grading"),
        ("kv", "HeyRwanda", "companion for exploring Rwanda"),
        ("kv", "Phibram", "call-center quality insight"),
        ("blank",),
        ("sec", "Contact"),
        ("kv", "Email", "doncdurkheim@gmail.com"),
        ("kv", "Web", "dondurkheim.com"),
        ("kv", "Company", "entelon.co"),
        ("kv", "LinkedIn", "dondurkheim"),
        ("kv", "Instagram", "don_durkheim"),
    ]


def dots(n):
    return f'<tspan class="d"> {"." * max(n, 1)} </tspan>'


def kv(key, value, width):
    fill = width - len(key) - len(value) - 3
    return f'<tspan class="k">{escape(key)}</tspan>:{dots(fill)}<tspan class="v">{escape(value)}</tspan>'


def render_row(row):
    kind = row[0]
    if kind == "title":
        return f'<tspan class="h">{escape(row[1])}</tspan>'
    if kind == "rule":
        return f'<tspan class="d">{"-" * INFO_W}</tspan>'
    if kind == "blank":
        return ""
    if kind == "sec":
        title = f"- {row[1]} "
        return f'<tspan class="h">{escape(title)}</tspan><tspan class="d">{"-" * (INFO_W - len(title))}</tspan>'
    if kind == "kv":
        return '<tspan class="d">. </tspan>' + kv(row[1], row[2], INFO_W - 2)
    raise ValueError(kind)


def svg(theme, art, info):
    c = THEMES[theme]
    art_cols = max(len(line) for line in art)
    info_x = PAD + art_cols * ART_CHAR_W + GAP
    width = round(info_x + INFO_W * CHAR_W + PAD)
    n = max(len(art), len(info))
    height = PAD * 2 + n * LINE_H
    art_top = (n - len(art)) // 2
    info_top = (n - len(info)) // 2
    y = lambda i: PAD + (i + 1) * LINE_H - 4
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="ConsolasFallback,Consolas,Menlo,\'Courier New\',monospace" '
        f'font-size="{FONT_SIZE}px">',
        f"<style>.a{{fill:{c['ascii']}}} .k{{fill:{c['key']}}} .v{{fill:{c['val']}}} "
        f".d{{fill:{c['dots']}}} .h{{fill:{c['head']};font-weight:bold}} text{{fill:{c['head']}}}</style>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>',
        '<text class="a" xml:space="preserve">',
    ]
    out += [f'<tspan x="{PAD}" y="{y(art_top + i)}">{escape(line)}</tspan>' for i, line in enumerate(art)]
    out += ["</text>", '<text xml:space="preserve">']
    for i, row in enumerate(info):
        body = render_row(row)
        if body:
            out.append(f'<tspan x="{info_x:.0f}" y="{y(info_top + i)}">{body}</tspan>')
    out += ["</text>", "</svg>"]
    return "\n".join(out) + "\n"


def main():
    info = rows(dt.date.today())
    for theme in THEMES:
        art = (HERE / f"ascii_{theme}.txt").read_text(encoding="utf-8").splitlines()
        (ROOT / f"{theme}_mode.svg").write_text(svg(theme, art, info), encoding="utf-8")


if __name__ == "__main__":
    main()
