#!/usr/bin/env python3
"""生成主页用的手绘风 SVG 资产。

设计语言（改这里就能整体换肤）：
  INK / INK2   深绿墨色，线稿与正文
  PAPER        米色纸，卡片底色
  RUST         赭红，印章、编号、强调箭头
  GOLD         芥末金，页脚与次强调
描边统一过 rough() 抖动滤镜；纸面叠 feTurbulence 颗粒。

用法：
  python3 tools/build_assets.py     # 重新生成 assets/*.svg
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

# ---------------------------------------------------------------- palette
INK = "#1F3B2C"
INK2 = "#33543F"
PAPER = "#F4EBD5"
RUST = "#A9472B"
GOLD = "#B8873A"

SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', Palatino, serif"
MONO = "'Courier New', 'Nimbus Mono PS', ui-monospace, monospace"

DEFS = """
  <defs>
    <filter id="rough" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.028" numOctaves="3" seed="11" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.4"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="rough2" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="5" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="3.6"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="grain">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="8"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
  </defs>
"""


# ---------------------------------------------------------------- helpers
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def jitter(pts, amount, seed):
    rnd = random.Random(seed)
    return [(x + rnd.uniform(-amount, amount), y + rnd.uniform(-amount, amount)) for x, y in pts]


def hand_path(pts, close=True):
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


def rough_rect(x, y, w, h, seed=1, step=46, jit=1.1):
    pts = []
    for i in range(0, int(w) + 1, step):
        pts.append((x + i, y))
    for i in range(0, int(h) + 1, step):
        pts.append((x + w, y + i))
    for i in range(0, int(w) + 1, step):
        pts.append((x + w - i, y + h))
    for i in range(0, int(h) + 1, step):
        pts.append((x, y + h - i))
    return hand_path(jitter(pts, jit, seed))


def rough_line(x1, y1, x2, y2, seed=1, seg=40, jit=0.9):
    n = max(2, int(math.dist((x1, y1), (x2, y2)) / seg))
    pts = [(x1 + (x2 - x1) * i / (n - 1), y1 + (y2 - y1) * i / (n - 1)) for i in range(n)]
    return hand_path(jitter(pts, jit, seed), close=False)


def grain(w, h, opacity=0.055):
    return (f'<rect x="0" y="0" width="{w}" height="{h}" fill="#8a7a5c" '
            f'filter="url(#grain)" opacity="{opacity}"/>')


def corner_ticks(w, h, pad=22, color=GOLD):
    s = 14
    out = []
    for cx, cy, sx, sy in ((pad, pad, 1, 1), (w - pad, pad, -1, 1),
                           (pad, h - pad, 1, -1), (w - pad, h - pad, -1, -1)):
        out.append(
            f'<path d="M {cx} {cy} l {sx*s} 0" stroke="{color}" stroke-width="1.4" opacity=".55"/>'
            f'<path d="M {cx} {cy} l 0 {sy*s}" stroke="{color}" stroke-width="1.4" opacity=".55"/>'
            f'<circle cx="{cx}" cy="{cy}" r="1.9" fill="{color}" opacity=".55"/>'
        )
    return "".join(out)


def paper_card(w, h, seed=1):
    """双层手绘纸边框 + 颗粒。"""
    return f"""  <g filter="url(#rough2)">
    <path d="{rough_rect(8, 8, w-16, h-16, seed=seed, step=54, jit=1.15)}" fill="{PAPER}" stroke="{INK}" stroke-width="1.7"/>
    <path d="{rough_rect(15, 15, w-30, h-30, seed=seed+17, step=54, jit=0.95)}" fill="none" stroke="{INK}" stroke-width="0.7" opacity=".3"/>
  </g>
  {grain(w, h, 0.05)}"""


# ---------------------------------------------------------------- hero
CAMERA = f"""
  <g stroke="{PAPER}" stroke-width="2.1" fill="none" stroke-linecap="round" opacity=".92" filter="url(#rough)">
    <path d="M 44 74 h 34 l 10 -12 h 24 l 10 12 h 22 a 6 6 0 0 1 6 6 v 38 a 6 6 0 0 1 -6 6 H 44 a 6 6 0 0 1 -6 -6 V 80 a 6 6 0 0 1 6 -6 Z"/>
    <circle cx="92" cy="97" r="19"/><circle cx="92" cy="97" r="11" opacity=".65"/>
    <path d="M 60 66 v -8 h 16 v 8"/><circle cx="148" cy="84" r="4"/>
    <path d="M 44 118 l 106 0" opacity=".35"/>
  </g>
  <text x="60" y="140" font-family="{MONO}" font-size="11" fill="{GOLD}" opacity=".85" letter-spacing="1.5">Zf</text>
"""

TERMINAL = f"""
  <g stroke="{PAPER}" stroke-width="2.1" fill="none" stroke-linecap="round" opacity=".92" filter="url(#rough)">
    <path d="M 18 18 h 132 a 5 5 0 0 1 5 5 v 84 a 5 5 0 0 1 -5 5 H 18 a 5 5 0 0 1 -5 -5 V 23 a 5 5 0 0 1 5 -5 Z"/>
    <path d="M 13 38 h 142" opacity=".5"/>
    <circle cx="26" cy="28" r="2.6"/><circle cx="36" cy="28" r="2.6"/><circle cx="46" cy="28" r="2.6"/>
    <path d="M 28 54 l 9 8 -9 8" stroke="{GOLD}"/>
    <path d="M 44 70 h 26" stroke="{GOLD}" opacity=".8"/>
    <path d="M 28 86 h 62" opacity=".35"/><path d="M 28 98 h 44" opacity=".25"/>
  </g>
"""


def hero():
    w, h = 1200, 372
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"
     aria-label="JAY201368 — Lingxiang Hu, Software Engineering, Nanjing University">
{DEFS}
  <linearGradient id="vg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#254834"/><stop offset="1" stop-color="#15291E"/>
  </linearGradient>
  <rect width="{w}" height="{h}" fill="{INK}"/>
  <rect width="{w}" height="{h}" fill="url(#vg)"/>
  {grain(w, h, 0.09)}

  <g filter="url(#rough2)" fill="none">
    <path d="{rough_rect(26, 24, w-52, h-48, seed=3, step=52, jit=1.4)}" stroke="{PAPER}" stroke-width="2.2" opacity=".85"/>
    <path d="{rough_rect(34, 32, w-68, h-64, seed=9, step=52, jit=1.2)}" stroke="{PAPER}" stroke-width="0.9" opacity=".4"/>
  </g>
  {corner_ticks(w, h, pad=20)}

  <g transform="translate(96 96)">{CAMERA}</g>
  <g transform="translate(950 96)">{TERMINAL}</g>

  <text x="{w/2}" y="150" text-anchor="middle" font-family="{SERIF}" font-size="82"
        fill="{PAPER}" letter-spacing="3">JAY201368</text>
  <path d="M 452 176 C 520 168, 680 184, 748 175" stroke="{GOLD}" stroke-width="2" fill="none"
        filter="url(#rough)" opacity=".9"/>
  <text x="{w/2}" y="212" text-anchor="middle" font-family="{MONO}" font-size="17"
        fill="{PAPER}" opacity=".82" letter-spacing="3.4">LINGXIANG HU</text>
  <text x="{w/2}" y="244" text-anchor="middle" font-family="{SERIF}" font-size="21"
        fill="{GOLD}" letter-spacing="1.2" font-style="italic">Software Engineering · Nanjing University</text>
  <text x="{w/2}" y="292" text-anchor="middle" font-family="{MONO}" font-size="12.5"
        fill="{PAPER}" opacity=".5" letter-spacing="4">AGENTS · PHOTO APPS · 2023</text>
</svg>
"""


# ---------------------------------------------------------------- divider
def rule():
    w, h = 1200, 46
    rays = []
    for i in range(8):
        a = math.pi * 2 * i / 8
        r1, r2 = 9.5, 15.5
        rays.append(f'<path d="M {600 + r1*math.cos(a):.1f} {23 + r1*math.sin(a):.1f} '
                    f'L {600 + r2*math.cos(a):.1f} {23 + r2*math.sin(a):.1f}"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">
{DEFS}
  <path d="M 30 23 C 200 19, 380 27, 556 23" stroke="{RUST}" stroke-width="2" fill="none"
        filter="url(#rough)" opacity=".8"/>
  <path d="M 644 23 C 820 27, 1000 19, 1170 23" stroke="{RUST}" stroke-width="2" fill="none"
        filter="url(#rough)" opacity=".8"/>
  <g stroke="{RUST}" stroke-width="1.4" fill="none" filter="url(#rough)" stroke-linecap="round">
    <circle cx="600" cy="23" r="5.5"/>{"".join(rays)}
  </g>
</svg>
"""


# ---------------------------------------------------------------- notes
W = 800
PAD = 56


def notes():
    rows = [
        dict(label="AGENTS", lead=True,
             sub="build · workflow · orchestration · engineering discipline",
             lines=["Local-first coding agents I build end to end: agent loop, tool",
                    "protocol, permission model, event trace. Alongside that I study",
                    "how they should be run — task graphs, isolated workers, and a",
                    "spec → tasks → review loop that ends in tested code."]),
        dict(label="PHOTOGRAPHY", color=RUST,
             lines=["Websites and small apps I wanted for my own shooting: light &",
                    "weather planning, RAW file handling. Built as much for how they",
                    "look and feel as for what they do."]),
        dict(label="SYSTEMS",
             lines=["Python and TypeScript by default; C++ / Metal only where it",
                    "actually pays off."]),
    ]
    y = 104
    body = []
    for i, row in enumerate(rows):
        lead = row.get("lead", False)
        size = 21.5 if lead else 20.5
        gap = 27
        if lead:
            body.append(f'<rect x="{PAD}" y="{y - 9}" width="7" height="7" fill="{RUST}"/>')
            body.append(f'<text x="{PAD + 16}" y="{y}" font-family="{MONO}" font-size="13" fill="{RUST}" letter-spacing="3.2">{row["label"]}</text>')
            body.append(f'<text x="{PAD + 122}" y="{y}" font-family="{SERIF}" font-size="15.5" font-style="italic" fill="{INK2}">{esc(row["sub"])}</text>')
        else:
            body.append(f'<text x="{PAD}" y="{y}" font-family="{MONO}" font-size="12.5" fill="{row.get("color", INK)}" letter-spacing="3.2">{row["label"]}</text>')
        for j, line in enumerate(row["lines"]):
            body.append(f'<text x="{PAD}" y="{y + (35 if lead else 29) + j*gap}" font-family="{SERIF}" font-size="{size}" fill="{INK}" opacity="{0.95 if lead else 0.9}">{esc(line)}</text>')
        y += (35 if lead else 29) + len(row["lines"]) * gap + (22 if lead else 16)
        if i < len(rows) - 1:
            body.append(f'<path d="{rough_line(PAD, y - 14, W - 46, y - 14, seed=20 + i, seg=60, jit=0.7)}" stroke="{INK}" stroke-width="0.9" opacity=".28" stroke-dasharray="2 6"/>')
            y += 34
    body = "\n  ".join(body)
    tools_y = y + 16
    h = tools_y + 54

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img"
     aria-label="Field notes. Agents: local-first coding agents built end to end — agent loop, tool protocol, permission model, event trace — and the workflow, orchestration and software-engineering discipline around them: task graphs, isolated workers, spec to tasks to review. Photography: websites and small apps I wanted for my own shooting. Systems: Python and TypeScript by default, C++ / Metal only where it pays off.">
{DEFS}
{paper_card(W, h, seed=4)}

  <text x="{PAD}" y="58" font-family="{MONO}" font-size="12.5" fill="{RUST}" letter-spacing="4.2">FIELD NOTES</text>
  <path d="{rough_line(PAD, 70, W - 46, 70, seed=6, seg=70, jit=0.7)}" stroke="{INK}" stroke-width="1" opacity=".45"/>
  <text x="{W - 46}" y="58" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{INK}" opacity=".5" letter-spacing="2">No. 01</text>
  <path d="{rough_line(34, 92, 34, h-26, seed=42, seg=70, jit=0.8)}" stroke="{RUST}" stroke-width="1.1" opacity=".35"/>

  {body}

  <path d="{rough_line(PAD, tools_y - 24, W - 46, tools_y - 24, seed=31, seg=80, jit=0.8)}" stroke="{INK}" stroke-width="1" opacity=".35"/>
  <text x="{PAD}" y="{tools_y}" font-family="{MONO}" font-size="12" fill="{INK}" opacity=".65" letter-spacing="1.1">TOOLS — Python · TypeScript · Swift · Vue · Docker · CMake</text>
</svg>
"""


# ---------------------------------------------------------------- cards
ICONS = {
    "maestro": f"""
      <g stroke="{INK}" stroke-width="1.9" fill="none" filter="url(#rough)" stroke-linecap="round">
        <circle cx="26" cy="16" r="8"/><circle cx="64" cy="44" r="8"/><circle cx="26" cy="72" r="8"/>
        <path d="M 34 20 L 56 40"/><path d="M 34 68 L 56 48"/><path d="M 26 24 L 26 64"/>
        <circle cx="64" cy="44" r="13" opacity=".3"/>
      </g>""",
    "codingagentneo": f"""
      <g stroke="{INK}" stroke-width="1.9" fill="none" filter="url(#rough)" stroke-linecap="round">
        <path d="M 6 12 h 76 a 4 4 0 0 1 4 4 v 52 a 4 4 0 0 1 -4 4 H 6 a 4 4 0 0 1 -4 -4 V 16 a 4 4 0 0 1 4 -4 Z"/>
        <path d="M 2 26 h 84" opacity=".45"/>
        <path d="M 18 40 l 8 7 -8 7"/><path d="M 33 54 h 18"/>
        <path d="M 62 40 h 16" opacity=".3"/><path d="M 62 49 h 10" opacity=".22"/>
      </g>""",
    "hikaridaily": f"""
      <g stroke="{INK}" stroke-width="1.9" fill="none" filter="url(#rough)" stroke-linecap="round">
        <path d="M 5 10 h 80 v 62 H 5 Z"/><path d="M 5 23 h 80"/>
        <path d="M 12 32 h 27 v 20 H 12 Z"/>
        <path d="M 46 32 h 31"/><path d="M 46 41 h 31"/><path d="M 46 50 h 22"/>
        <path d="M 12 61 h 61" opacity=".5"/><path d="M 12 65 h 61" opacity=".35"/>
        <circle cx="78" cy="17" r="3.6" stroke="{RUST}"/>
      </g>""",
    "zf2lumix": f"""
      <g stroke="{INK}" stroke-width="1.9" fill="none" filter="url(#rough)" stroke-linecap="round">
        <path d="M 8 20 h 24 l 7 -10 h 16 l 7 10 h 20 a 4 4 0 0 1 4 4 v 40 a 4 4 0 0 1 -4 4 H 8 a 4 4 0 0 1 -4 -4 V 24 a 4 4 0 0 1 4 -4 Z"/>
        <circle cx="43" cy="44" r="14"/><circle cx="43" cy="44" r="7.5" opacity=".55"/>
        <path d="M 74 35 h 7" opacity=".5"/>
        <g fill="{INK}" opacity=".5">
          <rect x="11" y="70" width="6" height="4"/><rect x="20" y="70" width="6" height="4"/>
          <rect x="29" y="70" width="6" height="4"/><rect x="38" y="70" width="6" height="4"/>
        </g>
      </g>""",
}


CW, CH = 430, 222


def card(num, title, lines, tags, live=None, icon="", kicker=""):
    w, h = CW, CH
    body = [f'<text x="28" y="{116 + i*23}" font-family="{SERIF}" font-size="16.5" fill="{INK}" opacity=".9">{esc(line)}</text>'
            for i, line in enumerate(lines)]
    chips, cx = [], 28
    for t in tags:
        tw = 11 + len(t) * 7.2
        chips.append(
            f'<rect x="{cx}" y="{h-52}" width="{tw:.0f}" height="20" rx="3" fill="none" stroke="{INK}" '
            f'stroke-width="1.1" opacity=".6" filter="url(#rough)"/>'
            f'<text x="{cx + tw/2:.0f}" y="{h-38}" text-anchor="middle" font-family="{MONO}" font-size="10.5" '
            f'fill="{INK}" opacity=".8" letter-spacing=".8">{esc(t)}</text>'
        )
        cx += tw + 9
    live_txt = ""
    if live:
        live_txt = (f'<text x="{w-30}" y="{h-38}" text-anchor="end" font-family="{MONO}" font-size="10.5" '
                    f'fill="{RUST}" letter-spacing="1.2">{esc(live)} ↗</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"
     aria-label="{title}: {' '.join(lines)}">
{DEFS}
{paper_card(w, h, seed=7 + num)}

  <text x="28" y="36" font-family="{MONO}" font-size="10.5" fill="{RUST}" letter-spacing="2">{kicker}</text>
  <text x="28" y="84" font-family="{SERIF}" font-size="30" fill="{INK}" letter-spacing="0.4">{title}</text>

  {"".join(body)}
  {"".join(chips)}
  {live_txt}

  <g transform="translate({w-78} 18) scale(0.5)">{icon}</g>
</svg>
"""


# ---------------------------------------------------------------- stamp
def stamp():
    w, h = 600, 118
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"
     aria-label="Nanjing University, Software Engineering, since 2023">
{DEFS}
  <g transform="rotate(-2.4 {w/2} {h/2})" opacity=".95">
    <g filter="url(#rough2)" fill="none" stroke="{RUST}">
      <path d="{rough_rect(8, 8, w-16, h-16, seed=5, step=44, jit=1.5)}" stroke-width="3.2"/>
      <path d="{rough_rect(17, 17, w-34, h-34, seed=11, step=44, jit=1.1)}" stroke-width="1" opacity=".7"/>
    </g>
    <text x="{w/2}" y="55" text-anchor="middle" font-family="{MONO}" font-size="22" fill="{RUST}"
          letter-spacing="6">NANJING UNIVERSITY</text>
    <text x="{w/2}" y="82" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{RUST}"
          letter-spacing="2.4" opacity=".85">SOFTWARE ENGINEERING · EST. 2023</text>
    <g fill="{RUST}" opacity=".8">
      <circle cx="26" cy="{h/2}" r="2.2"/><circle cx="{w-26}" cy="{h/2}" r="2.2"/>
    </g>
  </g>
</svg>
"""


# ---------------------------------------------------------------- footer
def footer():
    w, h = 1200, 148
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"
     aria-label="JAY201368 · Nanjing · 2023">
{DEFS}
  <linearGradient id="vg2" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#15291E"/><stop offset="1" stop-color="#254834"/>
  </linearGradient>
  <rect width="{w}" height="{h}" fill="{INK}"/>
  <rect width="{w}" height="{h}" fill="url(#vg2)"/>
  {grain(w, h, 0.09)}
  <path d="{rough_rect(26, 20, w-52, h-40, seed=33, step=54, jit=1.3)}" fill="none" stroke="{PAPER}"
        stroke-width="1.8" opacity=".8" filter="url(#rough2)"/>
  <g stroke="{PAPER}" stroke-width="1.6" fill="none" filter="url(#rough)" opacity=".75" transform="translate(600 58)">
    <path d="M -140 0 h 96"/><path d="M 44 0 h 96"/>
    <path d="M -30 0 c 8 -11 20 -11 28 0 c -8 11 -20 11 -28 0 Z"/>
    <circle cx="26" cy="0" r="4"/>
  </g>
  <text x="{w/2}" y="102" text-anchor="middle" font-family="{MONO}" font-size="18"
        fill="{GOLD}" letter-spacing="4.2">JAY201368 · NANJING · MMXXIII</text>
</svg>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "hero.svg": hero(),
        "rule.svg": rule(),
        "notes.svg": notes(),
        "stamp.svg": stamp(),
        "footer.svg": footer(),
        "card-maestro.svg": card(1, "maestro",
                                 ["Codex skill: worker orchestration, task",
                                  "dependencies, staged delivery."],
                                 ["Python"], live="docs", icon=ICONS["maestro"], kicker="ORCHESTRATION"),
        "card-codingagentneo.svg": card(2, "CodingAgentNeo",
                                        ["From scratch: agent loop, six tools,",
                                         "permissions, traces, SSE API, Vue GUI."],
                                        ["Python", "TypeScript"], icon=ICONS["codingagentneo"], kicker="AGENT RUNTIME"),
        "card-hikaridaily.svg": card(3, "HikariDaily",
                                     ["Weather newspaper: sun position, light",
                                      "windows, gear readings, a handbook."],
                                     ["TypeScript"], live="live", icon=ICONS["hikaridaily"], kicker="PHOTO APP"),
        "card-zf2lumix.svg": card(4, "zf2lumix",
                                  ["Nikon Zf NEF → S5M2 RW2, offline,",
                                   "with a filmstrip interface."],
                                  ["Python", "Metal"], live="live", icon=ICONS["zf2lumix"], kicker="PHOTO TOOL"),
    }
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"{name:26s} {len(svg):6d} B")


if __name__ == "__main__":
    main()
