"""
Driveway Sunlight — render the print flyer + IG square + FB landscape.
Run from the project root: python3 marketing/build_assets.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path("/Users/josh/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/32557ce1-683f-4dcb-96c6-4ad481710d68/c643fdcc-9301-421b-aa39-d011623727ed/skills/canvas-design/canvas-fonts")
OUT = ROOT / "marketing"

# Palette — Driveway Sunlight
NAVY        = (12, 41, 64)        # deep, trustworthy
NAVY_DEEP   = (8, 27, 45)
CREAM       = (250, 244, 230)     # paper-warm white
CREAM_DEEP  = (240, 230, 210)
SUN         = (248, 197, 70)      # the single accent
SUN_DEEP    = (210, 156, 36)
INK         = (24, 24, 24)
INK_SOFT    = (60, 65, 75)
RULE        = (200, 190, 170)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def fit_cover(img, target_w, target_h, focus_y=0.5):
    """Crop & resize image to fully cover target dimensions.
    focus_y: 0=top, 0.5=center, 1=bottom — where the interesting subject sits vertically."""
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = max(0, min(new_h - target_h, int((new_h - target_h) * focus_y)))
    return img.crop((left, top, left + target_w, top + target_h))


def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


# ============================================================
# PRINT FLYER — US Letter @ 200 DPI = 1700 x 2200
# ============================================================

def build_flyer():
    W, H = 1700, 2200
    canvas = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(canvas)

    margin = 90

    # --- Top eyebrow rule + label
    d.line([(margin, 130), (margin + 110, 130)], fill=NAVY, width=4)
    f_eyebrow = font("WorkSans-Bold.ttf", 22)
    d.text((margin + 130, 118), "QUEEN CREEK VILLAGES  ·  SUMMER 2026",
           font=f_eyebrow, fill=NAVY, spacing=2)

    # --- Massive name lockup
    f_name_big = font("BigShoulders-Bold.ttf", 220)
    d.text((margin - 8, 170), "ISAAC &", font=f_name_big, fill=NAVY)
    d.text((margin - 8, 360), "ELIJAH'S", font=f_name_big, fill=NAVY)

    # CAR WASH — set in the sun-yellow as the single accent moment
    f_carwash = font("BigShoulders-Bold.ttf", 260)
    d.text((margin - 14, 555), "CAR WASH", font=f_carwash, fill=SUN_DEEP)

    # Thin signature line
    f_sig = font("NothingYouCouldDo-Regular.ttf", 56)
    d.text((margin + 4, 820), "— hand-washed by the two of us.",
           font=f_sig, fill=INK_SOFT)

    # --- Portrait, contained left-side block
    portrait_src = Image.open(ROOT / "images/IMG_0308.jpeg").convert("RGB")
    p_w = 760
    p_h = 980
    portrait = fit_cover(portrait_src, p_w, p_h)
    # rounded mask
    mask = Image.new("L", (p_w, p_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, p_w, p_h), radius=28, fill=255)
    px, py = margin, 920
    canvas.paste(portrait, (px, py), mask)

    # subtle shadow plate behind the photo
    shadow = Image.new("RGBA", (p_w + 24, p_h + 24), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (12, 12, p_w + 12, p_h + 12), radius=32, fill=(12, 41, 64, 38)
    )
    canvas.paste(shadow, (px - 12, py - 12 + 4), shadow)
    canvas.paste(portrait, (px, py), mask)

    # --- Right column: the offer
    col_x = px + p_w + 70
    col_w = W - col_x - margin

    # $20 — the serif moment
    f_dollar = font("YoungSerif-Regular.ttf", 110)
    f_price  = font("YoungSerif-Regular.ttf", 320)
    d.text((col_x, 900), "$", font=f_dollar, fill=NAVY)
    d.text((col_x + 80, 830), "20", font=f_price, fill=NAVY)

    # FLAT — small caps under the price
    f_flat = font("WorkSans-Bold.ttf", 30)
    d.text((col_x + 4, 1180), "F L A T  ·  F U L L  E X T E R I O R",
           font=f_flat, fill=SUN_DEEP)

    # divider
    d.line([(col_x, 1235), (col_x + col_w - 40, 1235)], fill=RULE, width=2)

    # bullet list of what's included
    bullets = [
        "Pre-rinse + foam soap",
        "Hand-scrubbed top to bottom",
        "Brake dust decontamination on wheels",
        "Tires & rims cleaned",
        "Windows streak-free",
        "Hand-dried — no water spots",
    ]
    f_bullet = font("WorkSans-Regular.ttf", 30)
    by = 1275
    for b in bullets:
        # square bullet in sun-yellow
        d.rectangle((col_x, by + 12, col_x + 14, by + 26), fill=SUN_DEEP)
        # bolden the brake-dust line
        if "Brake dust" in b:
            d.text((col_x + 30, by), b, font=font("WorkSans-Bold.ttf", 30), fill=NAVY)
        else:
            d.text((col_x + 30, by), b, font=f_bullet, fill=INK)
        by += 55

    # --- Bottom contact strip — full-width navy bar
    strip_h = 480
    d.rectangle((0, H - strip_h, W, H), fill=NAVY)

    # right side of strip: QR (place first so we know available text width)
    qr = Image.open(ROOT / "images/qr-site.png").convert("RGB")
    qr_size = 280
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
    plate_pad = 20
    plate_x = W - margin - qr_size - plate_pad * 2
    plate_y = H - strip_h + 70
    rounded_rect(d, (plate_x, plate_y,
                     plate_x + qr_size + plate_pad * 2,
                     plate_y + qr_size + plate_pad * 2),
                 radius=18, fill=CREAM)
    canvas.paste(qr, (plate_x + plate_pad, plate_y + plate_pad))
    f_qcap = font("WorkSans-Bold.ttf", 20)
    cap = "SCAN FOR OUR SITE"
    tw, _ = text_size(d, cap, f_qcap)
    d.text((plate_x + plate_pad + qr_size // 2 - tw // 2,
            plate_y + qr_size + plate_pad * 2 + 14),
           cap, font=f_qcap, fill=SUN)

    # left side of strip: text + payment (kept inside plate_x boundary)
    sx = margin
    sy = H - strip_h + 80
    text_max_w = plate_x - sx - 40  # available width left of QR

    f_call = font("WorkSans-Bold.ttf", 32)
    d.text((sx, sy), "BOOK A WASH  ·  WE WALK TO YOU", font=f_call, fill=SUN)

    # Phone number — fit width by stepping size down if needed
    phone_label = "(480) 853-8729"
    for sz in (130, 120, 110, 100):
        f_phone_big = font("BigShoulders-Bold.ttf", sz)
        pw, ph = text_size(d, phone_label, f_phone_big)
        if pw <= text_max_w:
            break
    # TEXT pre-label sized to match optical height
    f_text_pre = font("WorkSans-Bold.ttf", 36)
    d.text((sx, sy + 70), "TEXT", font=f_text_pre, fill=SUN)
    tw_pre, _ = text_size(d, "TEXT", f_text_pre)
    d.text((sx + tw_pre + 24, sy + 56), phone_label, font=f_phone_big, fill=CREAM)

    f_sub = font("WorkSans-Regular.ttf", 26)
    d.text((sx, sy + 220),
           "Tell us your car, the date, and a good time.",
           font=f_sub, fill=(CREAM[0], CREAM[1], CREAM[2]))

    # payment chips
    chip_y = sy + 280
    chip_h = 54
    def chip(x, label):
        f = font("WorkSans-Bold.ttf", 22)
        tw, th = text_size(d, label, f)
        pad_x = 22
        w = tw + pad_x * 2
        rounded_rect(d, (x, chip_y, x + w, chip_y + chip_h),
                     radius=chip_h // 2, outline=SUN, width=3)
        d.text((x + pad_x, chip_y + (chip_h - th) // 2 - 4),
               label, font=f, fill=SUN)
        return x + w + 16

    nx = sx
    nx = chip(nx, "ZELLE  ·  same number")
    nx = chip(nx, "OR CASH")

    out_pdf = OUT / "flyer-print-letter.pdf"
    out_png = OUT / "flyer-print-letter.png"
    canvas.save(out_png, "PNG", optimize=True)
    canvas.save(out_pdf, "PDF", resolution=200.0)
    print(f"✓ flyer (print)  → {out_pdf.name}  +  {out_png.name}  ({W}x{H})")


# ============================================================
# INSTAGRAM SQUARE — 1080 x 1080
# ============================================================

def build_instagram():
    W, H = 1080, 1080
    canvas = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(canvas)

    # ------ Layout zones
    p_h = 620        # portrait height (top)
    strip_h = 230    # navy contact strip (bottom)
    mid_top = p_h
    mid_bot = H - strip_h  # 850

    # ------ TOP: portrait full-bleed
    portrait_src = Image.open(ROOT / "images/IMG_0308.jpeg").convert("RGB")
    portrait = fit_cover(portrait_src, W, p_h, focus_y=0.0)
    canvas.paste(portrait, (0, 0))

    # darken bottom of photo for legibility
    overlay = Image.new("RGBA", (W, 280), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(280):
        a = int(220 * (i / 280) ** 1.3)
        od.line([(0, i), (W, i)], fill=(8, 27, 45, a))
    canvas.paste(overlay, (0, p_h - 280), overlay)

    # yellow eyebrow chip top-left
    f_eb = font("WorkSans-Bold.ttf", 22)
    eyebrow = "QUEEN CREEK VILLAGES  ·  HAND CAR WASH"
    tw, th = text_size(d, eyebrow, f_eb)
    rounded_rect(d, (50, 50, 50 + tw + 40, 50 + th + 26),
                 radius=(th + 26) // 2, fill=SUN)
    d.text((50 + 20, 50 + 12), eyebrow, font=f_eb, fill=NAVY_DEEP)

    # Big name anchored to bottom of photo
    f_name = font("BigShoulders-Bold.ttf", 110)
    d.text((50, p_h - 210), "ISAAC & ELIJAH'S", font=f_name, fill=CREAM)
    d.text((50, p_h - 115), "CAR WASH", font=f_name, fill=SUN)

    # ------ MIDDLE: price + qualifier in the cream band (mid_top→mid_bot ≈ 620→850)
    mid_h = mid_bot - mid_top  # 230
    price_baseline = mid_top + 30  # top of price visual

    d.text((52, price_baseline + 32), "$",
           font=font("YoungSerif-Regular.ttf", 50), fill=NAVY)
    d.text((94, price_baseline),
           "20", font=font("YoungSerif-Regular.ttf", 140), fill=NAVY)

    # vertical divider
    d.line([(258, mid_top + 50), (258, mid_bot - 30)], fill=RULE, width=2)

    rx = 286
    d.text((rx, mid_top + 50), "FLAT  ·  FULL EXTERIOR HAND WASH",
           font=font("WorkSans-Bold.ttf", 24), fill=SUN_DEEP)
    d.text((rx, mid_top + 86),
           "Brake dust decon",
           font=font("WorkSans-Bold.ttf", 26), fill=NAVY)
    d.text((rx, mid_top + 124),
           "Hand-dried  ·  No water spots  ·  Tires + rims",
           font=font("WorkSans-Regular.ttf", 18), fill=INK_SOFT)
    d.text((rx, mid_top + 152),
           "We walk to you in Queen Creek Villages.",
           font=font("WorkSans-Italic.ttf", 16), fill=INK_SOFT)

    # ------ BOTTOM: navy contact strip
    strip_top = mid_bot
    d.rectangle((0, strip_top, W, H), fill=NAVY)

    # accent sun bar on the left side of strip
    d.rectangle((0, strip_top, 16, H), fill=SUN)

    d.text((52, strip_top + 32), "TEXT TO BOOK",
           font=font("WorkSans-Bold.ttf", 26), fill=SUN)

    d.text((50, strip_top + 66), "(480) 853-8729",
           font=font("BigShoulders-Bold.ttf", 88), fill=CREAM)

    d.text((52, strip_top + 180),
           "ZELLE TO SAME NUMBER  ·  OR CASH",
           font=font("WorkSans-Bold.ttf", 20), fill=SUN)

    out = OUT / "social-instagram-1080.png"
    canvas.save(out, "PNG", optimize=True)
    print(f"✓ instagram      → {out.name}  ({W}x{H})")


# ============================================================
# FACEBOOK LANDSCAPE — 1200 x 630
# ============================================================

def build_facebook():
    W, H = 1200, 630
    canvas = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(canvas)

    # Left column: portrait — wider so faces aren't crowded
    p_w = 440
    portrait_src = Image.open(ROOT / "images/IMG_0308.jpeg").convert("RGB")
    portrait = fit_cover(portrait_src, p_w, H, focus_y=0.1)
    canvas.paste(portrait, (0, 0))

    # Right column
    cx = p_w + 50
    cw = W - cx - 50

    # eyebrow
    f_eb = font("WorkSans-Bold.ttf", 18)
    d.text((cx, 48), "QUEEN CREEK VILLAGES  ·  SUMMER 2026", font=f_eb, fill=NAVY)
    d.line([(cx, 82), (cx + 50, 82)], fill=SUN_DEEP, width=4)

    # name lockup
    d.text((cx - 4, 96), "ISAAC & ELIJAH'S",
           font=font("BigShoulders-Bold.ttf", 80), fill=NAVY)
    d.text((cx - 6, 170), "CAR WASH",
           font=font("BigShoulders-Bold.ttf", 110), fill=SUN_DEEP)

    # $20 row
    py = 310
    d.text((cx, py + 8), "$", font=font("YoungSerif-Regular.ttf", 60), fill=NAVY)
    d.text((cx + 44, py - 26), "20", font=font("YoungSerif-Regular.ttf", 120), fill=NAVY)

    # vertical divider
    d.line([(cx + 190, py), (cx + 190, py + 130)], fill=RULE, width=2)

    # qualifier next to price
    d.text((cx + 210, py + 4), "FLAT  ·  FULL EXTERIOR",
           font=font("WorkSans-Bold.ttf", 22), fill=NAVY)
    d.text((cx + 210, py + 38),
           "Hand-washed  ·  Brake dust decon",
           font=font("WorkSans-Regular.ttf", 18), fill=INK_SOFT)
    d.text((cx + 210, py + 62),
           "No water spots  ·  Tires + rims",
           font=font("WorkSans-Regular.ttf", 18), fill=INK_SOFT)

    # bottom navy strip (no QR for social — viewer can't scan their own screen)
    strip_h = 170
    strip_top = H - strip_h
    d.rectangle((0, strip_top, W, H), fill=NAVY)
    d.rectangle((0, strip_top, 14, H), fill=SUN)

    sx = cx - 4
    d.text((sx, strip_top + 20), "TEXT TO BOOK",
           font=font("WorkSans-Bold.ttf", 18), fill=SUN)
    d.text((sx, strip_top + 44), "(480) 853-8729",
           font=font("BigShoulders-Bold.ttf", 62), fill=CREAM)
    d.text((sx, strip_top + 130),
           "ZELLE TO SAME NUMBER  ·  OR CASH",
           font=font("WorkSans-Bold.ttf", 16), fill=SUN)

    out = OUT / "social-facebook-1200x630.png"
    canvas.save(out, "PNG", optimize=True)
    print(f"✓ facebook       → {out.name}  ({W}x{H})")


# ============================================================
# OG LINK PREVIEW — hero-style, 1200 x 630
# Full-bleed photo + big overlay type + yellow $20 seal.
# This is the card that renders in iMessage / WhatsApp / FB.
# ============================================================

def build_og_hero():
    W, H = 1200, 630
    canvas = Image.new("RGB", (W, H), NAVY_DEEP)
    d = ImageDraw.Draw(canvas)

    # Full-bleed portrait — bias toward top so faces stay in frame.
    # Source is portrait (0.75 ratio); target is wide (1.9 ratio) so the
    # crop is aggressive vertically — focus_y=0 keeps the boys' heads.
    portrait_src = Image.open(ROOT / "images/IMG_0308.jpeg").convert("RGB")
    portrait = fit_cover(portrait_src, W, H, focus_y=0.05)
    canvas.paste(portrait, (0, 0))

    # Cinematic dual gradient: dark at top for eyebrow, deeper dark at bottom
    # for the headline + phone line. Middle stays clear so the boys read.
    top_overlay = Image.new("RGBA", (W, 180), (0, 0, 0, 0))
    od = ImageDraw.Draw(top_overlay)
    for i in range(180):
        a = int(160 * (1 - i / 180) ** 1.2)
        od.line([(0, i), (W, i)], fill=(8, 20, 35, a))
    canvas.paste(top_overlay, (0, 0), top_overlay)

    bot_overlay = Image.new("RGBA", (W, 380), (0, 0, 0, 0))
    od = ImageDraw.Draw(bot_overlay)
    for i in range(380):
        a = int(225 * (i / 380) ** 1.3)
        od.line([(0, i), (W, i)], fill=(8, 20, 35, a))
    canvas.paste(bot_overlay, (0, H - 380), bot_overlay)

    # --- Top eyebrow
    f_eb = font("WorkSans-Bold.ttf", 22)
    d.text((50, 40), "QUEEN CREEK VILLAGES  ·  SUMMER 2026",
           font=f_eb, fill=SUN)
    d.line([(50, 78), (110, 78)], fill=SUN, width=3)

    # --- Massive headline lockup (left-anchored, lower-middle)
    headline_y = 320
    d.text((46, headline_y),
           "ISAAC & ELIJAH'S",
           font=font("BigShoulders-Bold.ttf", 90), fill=CREAM)
    d.text((44, headline_y + 78),
           "CAR WASH",
           font=font("BigShoulders-Bold.ttf", 140), fill=SUN)

    # --- $20 seal: circular yellow medallion top-right
    # Drawn at 4x then downsampled for crisp edges.
    s_diam = 230
    seal = Image.new("RGBA", (s_diam * 4, s_diam * 4), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seal)
    sd.ellipse((0, 0, s_diam * 4 - 1, s_diam * 4 - 1), fill=SUN)
    seal = seal.resize((s_diam, s_diam), Image.LANCZOS)
    sx = W - s_diam - 50
    sy = 50
    # subtle drop shadow
    shadow = Image.new("RGBA", (s_diam + 24, s_diam + 24), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse(
        (12, 16, s_diam + 12, s_diam + 16), fill=(0, 0, 0, 90)
    )
    canvas.paste(shadow, (sx - 12, sy - 12 + 6), shadow)
    canvas.paste(seal, (sx, sy), seal)

    # seal contents — "$" + "20" + "FLAT WASH"
    # measure to center inside the circle
    f_seal_dollar = font("YoungSerif-Regular.ttf", 56)
    f_seal_price  = font("YoungSerif-Regular.ttf", 130)
    f_seal_sub    = font("WorkSans-Bold.ttf", 20)

    price_str = "20"
    dollar_w, _ = text_size(d, "$", f_seal_dollar)
    price_w, _  = text_size(d, price_str, f_seal_price)
    total_w = dollar_w + 4 + price_w
    px = sx + (s_diam - total_w) // 2
    py = sy + 38
    d.text((px, py + 28), "$", font=f_seal_dollar, fill=NAVY_DEEP)
    d.text((px + dollar_w + 4, py), price_str,
           font=f_seal_price, fill=NAVY_DEEP)

    # "FLAT WASH" curving below
    sub = "FLAT WASH"
    sub_w, _ = text_size(d, sub, f_seal_sub)
    d.text((sx + (s_diam - sub_w) // 2, sy + s_diam - 56),
           sub, font=f_seal_sub, fill=NAVY_DEEP)

    # tiny radial pips
    pip_color = NAVY_DEEP
    cx_s = sx + s_diam // 2
    cy_s = sy + s_diam // 2
    import math
    for i in range(12):
        ang = (math.pi * 2) * (i / 12)
        x = cx_s + math.cos(ang) * (s_diam // 2 - 14)
        y = cy_s + math.sin(ang) * (s_diam // 2 - 14)
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=pip_color)

    # --- Bottom phone strip: subtle sun rule + the phone in cream
    # Yellow rule
    d.rectangle((46, H - 96, 76, H - 92), fill=SUN)

    d.text((46, H - 80),
           "TEXT TO BOOK",
           font=font("WorkSans-Bold.ttf", 20), fill=SUN)
    d.text((44, H - 56),
           "(480) 853-8729",
           font=font("BigShoulders-Bold.ttf", 60), fill=CREAM)

    # tagline on the right, balancing the phone
    f_tag = font("WorkSans-Bold.ttf", 18)
    tag = "HAND-WASHED  ·  BRAKE DUST DECON  ·  NO WATER SPOTS"
    tw, _ = text_size(d, tag, f_tag)
    d.text((W - tw - 50, H - 38), tag, font=f_tag, fill=SUN)

    out_marketing = OUT / "social-og-hero-1200x630.png"
    out_deployed  = ROOT / "images" / "og-preview.png"
    canvas.save(out_marketing, "PNG", optimize=True)
    canvas.save(out_deployed, "PNG", optimize=True)
    print(f"✓ og hero       → {out_marketing.name}  +  images/og-preview.png  ({W}x{H})")


if __name__ == "__main__":
    build_flyer()
    build_instagram()
    build_facebook()
    build_og_hero()
