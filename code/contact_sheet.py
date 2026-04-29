"""
Builds charts/_contact_sheet.png — all charts tiled in a 3-column grid at thumbnail size.
Uses PIL (Pillow) to compose. Requires no Plotly at runtime.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")

# Ordered list: (filename_stem, slide_number)
CHART_ORDER = [
    ("hero_1_divergence",        "Slide 2"),
    ("cascade_1_fertilizer_lag", "Slide 7"),
    ("cascade_2_defence_backlog","Slide 8"),
    ("hero_2_fx_pca",            "Slide 9"),
    ("cascade_4_sticky_cpi",     "Slide 10"),
    ("portfolio_risk_donut",     "Slide 11"),
    ("hero_3_backtest",          "Slide 13"),
    ("hero_3_stress_table",      "Slide 13"),
    ("risk_polymarket",          "Slide 16"),
    ("scenario_pl",              "Slide 14"),
]

COLS        = 3
THUMB_W     = 460
THUMB_H     = 270
PAD         = 14
LABEL_H     = 22
BG_COLOR    = (240, 242, 246)
BORDER_CLR  = (10, 22, 40)   # NAVY
LABEL_CLR   = (10, 22, 40)

def build_contact_sheet():
    rows = math.ceil(len(CHART_ORDER) / COLS)
    canvas_w = COLS * (THUMB_W + PAD) + PAD
    canvas_h = rows * (THUMB_H + LABEL_H + PAD) + PAD + 50  # +50 for header

    canvas = Image.new("RGB", (canvas_w, canvas_h), BG_COLOR)
    draw   = ImageDraw.Draw(canvas)

    # Header
    try:
        font_hdr = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        font_lbl = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11)
    except:
        font_hdr = ImageFont.load_default()
        font_lbl = ImageFont.load_default()

    draw.text((PAD, PAD), "Citi Global Markets 2026 — Chart Contact Sheet", font=font_hdr, fill=LABEL_CLR)

    for idx, (stem, slide_lbl) in enumerate(CHART_ORDER):
        path = os.path.join(CHARTS_DIR, f"{stem}.png")
        row  = idx // COLS
        col  = idx % COLS

        x = PAD + col * (THUMB_W + PAD)
        y = 50 + PAD + row * (THUMB_H + LABEL_H + PAD)

        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            img.thumbnail((THUMB_W, THUMB_H), Image.LANCZOS)

            # Paste centred in thumbnail cell
            paste_x = x + (THUMB_W - img.width) // 2
            paste_y = y + (THUMB_H - img.height) // 2
            canvas.paste(img, (paste_x, paste_y))

            # Border
            draw.rectangle([x-1, y-1, x+THUMB_W, y+THUMB_H], outline=BORDER_CLR, width=1)
        else:
            # Placeholder box
            draw.rectangle([x, y, x+THUMB_W, y+THUMB_H], fill=(220, 220, 220), outline=BORDER_CLR)
            draw.text((x + 10, y + THUMB_H // 2 - 8), "MISSING", font=font_lbl, fill=(180, 0, 0))

        # Label below thumbnail
        label = f"{slide_lbl} — {stem}"
        draw.text((x, y + THUMB_H + 3), label, font=font_lbl, fill=LABEL_CLR)

    out = os.path.join(CHARTS_DIR, "_contact_sheet.png")
    canvas.save(out, dpi=(144, 144))
    print(f"Saved → {out}")
    return out

if __name__ == "__main__":
    build_contact_sheet()
