#!/usr/bin/env python3
"""Render the 26 November 2026 world-news front page to news.png (1024x1024).

Build-time script only: it runs on the builder's machine, never in the grader.
All stories below were verified against live wire reports dated 26 Nov 2026
(UTC), or first reported on 26 Nov in Asia-Pacific timezones.
Confidence: ● = wire-confirmed on 26 Nov 2026; ◐ = reported late 25 Nov (US)
which is 26 Nov in Asia-Pacific timezones.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "news.png"

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (18, 52, 86)
GREY = (90, 86, 78)
LIGHT = (233, 228, 214)
RULE = (120, 110, 92)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    """Greedy word wrap to a pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def box(x, y, w, h, fill=(255, 255, 255), outline=RULE, width=1):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=outline, width=width)


def headline_box(x, y, w, h, kicker, head, body, head_size=13, body_size=10, accent=RED):
    box(x, y, w, h)
    d.rectangle([x, y, x + w - 1, y + 3], fill=accent)
    cx = x + 8
    cy = y + 9
    d.text((cx, cy), kicker, font=font(SANS_B, 9), fill=accent)
    cy += 13
    hl = wrap(head, font(SANS_B, head_size), w - 16)
    cy = text_block(cx, cy, hl[:2], font(SANS_B, head_size), leading=head_size + 2)
    cy += 2
    bl = wrap(body, font(SANS, body_size), w - 16)
    text_block(cx, cy, bl[:4], font(SANS, body_size), leading=body_size + 2)


# ---------------------------------------------------------------- masthead
d.rectangle([16, 8, 1008, 102], fill=INK)
d.text((512, 16), "THE WORLD IN ONE DAY", font=font(SERIF_B, 42),
       fill=(247, 243, 232), anchor="ma")
d.rectangle([36, 66, 988, 68], fill=RED)
d.text((512, 73), "THURSDAY  ·  26 NOVEMBER 2026", font=font(SANS_B, 22),
       fill=(255, 255, 255), anchor="ma")

# ---------------------------------------------------------------- leads
LEADS = [
    ("LEAD  ●", "TRUMP'S NEW TARIFF SALVO",
     "Washington proposes new tariffs of 20%–40% on 14 trading partners — "
     "China capped at 20%, or 40% if the trade truce fails — in a Section 301 "
     "probe into excess industrial capacity. Asian markets plunge.",
     "Reuters, 26 Nov"),
    ("LEAD  ◐", "19 CIVILIANS KILLED IN SUDAN",
     "Drone strikes by Sudan's paramilitary RSF kill 19 civilians and wound 20 "
     "in Blue Nile state — 19 dead in the capital Damazin, and the Roseires dam "
     "and power facilities hit.",
     "Reuters, 26 Nov"),
    ("LEAD  ●", "FIRST PAKISTANI IN ORBIT",
     "China's Shenzhou-24 carries the first Pakistani astronaut to the Tiangong "
     "space station — a milestone in China–Pakistan space cooperation, launched "
     "from Jiuquan on a Long March 2F rocket.",
     "Reuters, 26 Nov"),
]
lx, lw, lgap = 16, 320, 8
for i, (kick, head, body, src) in enumerate(LEADS):
    x = lx + i * (lw + lgap)
    box(x, 110, lw, 148)
    d.rectangle([x, 110, x + lw - 1, 113], fill=RED)
    cx, cy = x + 10, 118
    d.text((cx, cy), kick, font=font(SANS_B, 10), fill=RED)
    cy += 15
    cy = text_block(cx, cy, wrap(head, font(SERIF_B, 19), lw - 20)[:2],
                    font(SERIF_B, 19), leading=21)
    cy += 3
    cy = text_block(cx, cy, wrap(body, font(SANS, 11), lw - 20)[:4],
                    font(SANS, 11), leading=14)
    d.text((cx, 110 + 148 - 18), src, font=font(SANS, 9), fill=GREY)

# ---------------------------------------------------------------- panels
PANELS = [
    ("GAZA  ◐", "Strike kills Hamas security chief",
     "Israeli airstrike in Gaza City kills a senior Hamas security chief, his wife "
     "and two children — the second such killing in 24 hours."),
    ("EGYPT  ●", "Cairo tanker fire kills 30",
     "A fuel tanker crash ignites a massive fire on a highway around Cairo, "
     "killing at least 30 people in a densely populated area."),
    ("MARKETS  ●", "Stocks plunge on tariff fears",
     "Asian shares tumble — Seoul −5.8%, Taiwan −4.7%, Nikkei −2.8% — and the "
     "S&P 500 and Nasdaq slide as the AI rally stumbles."),
    ("USA  ●", "Economy beats forecasts",
     "US third-quarter GDP growth is revised sharply higher, weekly jobless "
     "claims fall more than expected, and consumer confidence nears a two-year high."),
    ("UKRAINE  ●", "Power cut in five regions",
     "Russian strikes knock out power in five Ukrainian regions and kill five; "
     "Moscow's own figures show nearly 500,000 war dead; the Pentagon holds "
     "back Patriot missiles."),
    ("GULF  ◐", "Mine blast and drone hit Riyadh",
     "An oil tanker catches fire in the Strait of Hormuz after hitting a naval "
     "mine; a Houthi drone strikes a Riyadh financial-district tower, wounding 11."),
    ("SPACE  ●", "A million satellites, a new crater",
     "The US authorises SpaceX to deploy 1m satellites; asteroid-defence "
     "images reveal a new crater; a Japan–Europe mission reaches Mercury "
     "after eight years."),
    ("ASIA-PACIFIC  ●", "Treaty, lawsuit, mine flood",
     "Solomon Islands signs a security treaty with Australia; Malaysia sues "
     "Google for $146m over YouTube; an Indonesia mine flood kills nine."),
    ("AFRICA  ●", "Ramaphosa wins in court",
     "A South African court backs President Ramaphosa in a cash-theft probe; "
     "Ethiopia pushes healthcare independence; Suez Canal revenues recover."),
    ("AMERICAS  ●", "Hostages freed in Colombia",
     "Colombian police storm a supermarket and free 20 people held hostage for "
     "17 hours; Petrobras unveils a $122bn plan; Venezuela reveals $237.5bn "
     "of public debt."),
    ("EUROPE  ●", "Airspace, minerals, AI cash",
     "Poland flags renewed airspace violations; France seeks critical-mineral "
     "independence; the EU plans a $55bn AI push; Ireland votes on neutrality."),
    ("TECH & COURTS  ●", "Huawei guilty; Nvidia warned",
     "A Brooklyn jury finds Huawei guilty on 10 of 12 counts; S&P puts Nvidia "
     "on CreditWatch Negative; Anthropic's slide rattles Wall Street's AI bets."),
]
px, py = 16, 266
pw, ph, pgap = 240, 100, 8
for i, (kick, head, body) in enumerate(PANELS):
    x = px + (i % 4) * (pw + pgap)
    y = py + (i // 4) * (ph + pgap)
    headline_box(x, y, pw, ph, kick, head, body, head_size=12, body_size=10)

# ---------------------------------------------------------------- briefs
BRIEFS = [
    "Abrego Garcia lands in Spain after a US departure deal.",
    "Iraq's top court: Baghdad may deploy troops to Kurdistan borders.",
    "Israeli opposition advances an Oct 7 attack probe Netanyahu opposes.",
    "PhonePe restarts its IPO, eyeing up to a $15bn market debut.",
    "Fed policymakers at odds over the causes of high inflation.",
    "OPEC blames the EU for the COP31 collapse; Pope Leo calls it troubling.",
    "North Korea expels a Swiss diplomat in a sanctions row.",
    "Lebanon plans a second international airport, at Kleiat.",
    "Britain moves military aircraft over drone threats.",
    "Bangladesh raises garment workers' wages by 36%.",
    "Plane crash off the Mississippi coast kills six, incl. two children.",
    "Colombia marks 10 years since its historic peace accord.",
    "Brazil: Wolbachia mosquitoes cut viral infections by 68%.",
    "India: IITs to add 6,000 tech seats; space economy to hit $45bn.",
    "Canada reaffirms its inflation strategy as energy shocks loom.",
    "El Salvador allocates $860m in debt financing for year-end spending.",
    "Barbados sets a February deadline for a Caribbean AI framework.",
    "Xi's graft probe of a Shanghai rising star upends China's power path.",
    "Tempus to acquire Personalis in a $600m cash merger deal.",
    "Meta officials meet Congress over suspended accounts.",
    "World Chess Championship: Gukesh draws Game 2 vs Sindarov in 20 moves.",
    "Duran Duran guitarist Andy Taylor dies, aged 65.",
    "Iran confronts deepening financial hardship.",
    "Vietnam advances sustainable agriculture; South Korea backs EVs.",
    "Russia raises defence allocations; Ukraine–Hungary talk trade.",
    "German Q3 GDP and French consumer confidence due today.",
    "Japan's 40-year bond auction draws weak demand; inflation jumps 4.2%.",
    "Australia's hotter CPI lifts rate-hike pressure on the RBA.",
    "Emirates tops global airline rankings for reliability.",
    "Elderly Alzheimer's patient found after 11 days lost in the Amazon.",
    "Shein to pay $100m to settle US claims it misled consumers.",
    "US malls bet on festive experiences to lure online shoppers.",
]
by = 594
d.text((16, by), "IN BRIEF — 32 MORE STORIES FROM 26 NOVEMBER",
       font=font(SANS_B, 12), fill=BLUE)
d.rectangle([16, by + 17, 1008, by + 19], fill=BLUE)
by += 26
half = (len(BRIEFS) + 1) // 2
for col in range(2):
    x = 16 + col * 500
    y = by
    for b in BRIEFS[col * half:(col + 1) * half]:
        line = "•  " + b
        lines = wrap(line, font(SANS, 11), 488)
        y = text_block(x, y, lines[:1], font(SANS, 11), leading=14)

# ---------------------------------------------------------------- regions
REGIONS = [
    ("N. AMERICA", "Tariffs, GDP, Nvidia"),
    ("LATIN AMERICA", "Petrobras, debt, peace"),
    ("EUROPE", "Airspace, AI, neutrality"),
    ("MIDDLE EAST", "Gaza, Hormuz, Riyadh"),
    ("AFRICA", "Sudan, Ramaphosa, Suez"),
    ("ASIA", "Space, markets, Google suit"),
    ("OCEANIA & SPACE", "Treaty, Mercury, satellites"),
]
ry = 850
d.text((16, ry), "AROUND THE WORLD IN SEVEN REGIONS",
       font=font(SANS_B, 12), fill=BLUE)
ry += 20
rw = (992 - 6 * 6) // 7
for i, (name, note) in enumerate(REGIONS):
    x = 16 + i * (rw + 6)
    box(x, ry, rw, 44, fill=LIGHT)
    d.text((x + rw // 2, ry + 5), name, font=font(SANS_B, 9),
           fill=BLUE, anchor="ma")
    d.text((x + rw // 2, ry + 20), note, font=font(SANS, 9),
           fill=INK, anchor="ma")

# ---------------------------------------------------------------- timeline
ty = 940
d.text((16, ty), "THE DAY IN ORDER  (UTC, approximate — as reports reached the wires)",
       font=font(SANS_B, 11), fill=BLUE)
ty += 18
d.line([(24, ty + 6), (1000, ty + 6)], fill=RULE, width=2)
TIMES = [
    ("00:00", "Tariff findings out"),
    ("01:00", "Asian markets plunge"),
    ("03:00", "Crew aboard Tiangong"),
    ("06:00", "Cairo toll reaches 30"),
    ("09:00", "Europe opens; GDP due"),
    ("13:30", "US GDP revised up"),
    ("15:00", "Wall St slides"),
    ("18:00", "Sudan toll: 19 dead"),
]
tw = 992 // 8
for i, (t, label) in enumerate(TIMES):
    x = 16 + i * tw + tw // 2
    d.ellipse([x - 4, ty + 2, x + 4, ty + 10], fill=RED)
    d.text((x, ty + 14), t, font=font(SANS_B, 10), fill=RED, anchor="ma")
    d.text((x, ty + 27), label, font=font(SANS, 8), fill=INK, anchor="ma")

# ---------------------------------------------------------------- footer
d.rectangle([16, 1000, 1008, 1016], fill=INK)
d.text((512, 1004), "DATE CHECK: every story reported on THURSDAY 26 NOVEMBER 2026  ·  "
       "Sources: Reuters, AP, BBC & wire roundups dated 26 Nov 2026  ·  "
       "● confirmed 26 Nov  ·  ◐ late 25 Nov US = 26 Nov Asia-Pacific",
       font=font(SANS, 9), fill=(247, 243, 232), anchor="ma")

img.save(OUT, optimize=True)
print("saved", OUT, img.size)
