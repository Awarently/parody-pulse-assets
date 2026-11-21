#!/usr/bin/env python3
"""Add the Parody Pulse header (with date) and footer to an article body image.

Usage:
  python stamp.py body.png                      # output: body_final.png, date = current month
  python stamp.py body.png -o out.png --date "December 2026"

Requires: pip install pillow
Header/footer are scaled to the body image width.
"""
import argparse, datetime, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HEADER = os.path.join(HERE, "header", "ParodyPulse_Header_Base_NoDate.png")
FOOTER = os.path.join(HERE, "footer", "ParodyPulse_Footer.png")
FONT = os.path.join(HERE, "fonts", "LibreBaskerville.ttf")
DATE_RIGHT, DATE_BASELINE, DATE_SIZE = 1068, 26, 20  # px on the 1080-wide base
DATE_MAX_WIDTH = 128  # date must stay right of the dome (left edge x=940)


def make_header(date_text, scale=2):
    base = Image.open(HEADER).convert("RGB")
    w, h = base.size
    big = base.resize((w * scale, h * scale), Image.LANCZOS)
    size = DATE_SIZE * scale
    while True:
        font = ImageFont.truetype(FONT, size)
        try:
            font.set_variation_by_axes([400])
        except Exception:
            pass
        if font.getlength(date_text) <= DATE_MAX_WIDTH * scale or size < 10 * scale:
            break
        size -= 1
    shadow = Image.new("RGBA", big.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((DATE_RIGHT * scale, DATE_BASELINE * scale + 2), date_text,
                                font=font, fill=(0, 0, 0, 110), anchor="rs")
    shadow = shadow.filter(ImageFilter.GaussianBlur(scale))
    big = Image.alpha_composite(big.convert("RGBA"), shadow)
    ImageDraw.Draw(big).text((DATE_RIGHT * scale, DATE_BASELINE * scale), date_text,
                             font=font, fill="white", anchor="rs")
    return big.convert("RGB")


def fit_width(img, width):
    if img.width == width:
        return img
    return img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("body")
    p.add_argument("-o", "--output")
    p.add_argument("--date", default=datetime.date.today().strftime("%B %Y"))
    a = p.parse_args()
    body = Image.open(a.body).convert("RGB")
    W = body.width
    parts = [fit_width(make_header(a.date), W), body, fit_width(Image.open(FOOTER).convert("RGB"), W)]
    out = Image.new("RGB", (W, sum(i.height for i in parts)), "white")
    y = 0
    for i in parts:
        out.paste(i, (0, y)); y += i.height
    path = a.output or os.path.splitext(a.body)[0] + "_final.png"
    out.save(path)
    print(path, out.size)


if __name__ == "__main__":
    main()
