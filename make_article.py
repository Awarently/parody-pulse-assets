#!/usr/bin/env python3
"""Make a complete Parody Pulse article: AI-generated body + standard header (today's date) + footer.

Usage:
  python make_article.py --headline "..." --subhead "..." --text "..." --scene "..." [--date "December 2026"] [-o out.png]
  python make_article.py ... --provider gemini
  python make_article.py ... --dry-run          # print the image prompt, no API call

Keys (env var or a .env file next to this script):
  OPENAI_API_KEY   (default provider; model via OPENAI_IMAGE_MODEL, default gpt-image-1)
  GEMINI_API_KEY   (--provider gemini; model via GEMINI_IMAGE_MODEL, default gemini-2.5-flash-image)
An API key is separate from a ChatGPT or Gemini subscription. Create one on the provider's developer site.
"""
import argparse, base64, io, json, os, re, sys, urllib.request, urllib.error
from datetime import date
from PIL import Image
import stamp

HERE = os.path.dirname(os.path.abspath(__file__))

STYLE = """Create the BODY of a satirical newspaper front page as a single image, 1:1 square.
Do NOT draw any masthead, logo, title bar or footer: those are added later. Start directly with the headline at the top edge.
Layout, top to bottom, on a clean white page:
1. Headline: very large, heavy black serif (Playfair/Times Bold style), max 2 lines, exactly this text: "{headline}"
2. Subhead: italic serif, dark gray, 2 lines, exactly this text: "{subhead}"
3. One wide photorealistic photograph, edge to edge, about 55% of the page height. Scene: {scene}
4. Body paragraph: black serif, 4 lines, exactly this text: "{text}"
Spell all text exactly as given. No other text, no watermarks, no logos of real organizations."""


def load_env():
    p = os.path.join(HERE, ".env")
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r"\s*([A-Z_]+)\s*=\s*(.+?)\s*$", line)
            if m and m.group(1) not in os.environ:
                os.environ[m.group(1)] = m.group(2).strip("'\"")


def post(url, payload, headers):
    req = urllib.request.Request(url, json.dumps(payload).encode(), {"Content-Type": "application/json", **headers})
    try:
        return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        sys.exit(f"API error {e.code}: {e.read().decode()[:500]}")


def gen_openai(prompt):
    key = os.environ.get("OPENAI_API_KEY") or sys.exit("OPENAI_API_KEY not set")
    r = post("https://api.openai.com/v1/images/generations",
             {"model": os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1"), "prompt": prompt,
              "size": "1024x1024", "n": 1},
             {"Authorization": f"Bearer {key}"})
    return base64.b64decode(r["data"][0]["b64_json"])


def gen_gemini(prompt):
    key = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY not set")
    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
    r = post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
             {"contents": [{"parts": [{"text": prompt}]}]}, {"x-goog-api-key": key})
    for part in r["candidates"][0]["content"]["parts"]:
        d = part.get("inlineData") or part.get("inline_data")
        if d:
            return base64.b64decode(d["data"])
    sys.exit("Gemini returned no image: " + json.dumps(r)[:500])


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--headline", required=True)
    a.add_argument("--subhead", required=True)
    a.add_argument("--text", required=True)
    a.add_argument("--scene", required=True)
    a.add_argument("--date", default=date.today().strftime("%B %Y"))
    a.add_argument("--provider", choices=["openai", "gemini"], default="openai")
    a.add_argument("-o", "--output")
    a.add_argument("--dry-run", action="store_true")
    a = a.parse_args()
    prompt = STYLE.format(headline=a.headline, subhead=a.subhead, scene=a.scene, text=a.text)
    if a.dry_run:
        print(prompt); return
    load_env()
    raw = (gen_openai if a.provider == "openai" else gen_gemini)(prompt)
    body = Image.open(io.BytesIO(raw)).convert("RGB")
    slug = re.sub(r"[^a-z0-9]+", "-", a.headline.lower()).strip("-")[:50]
    out_dir = os.path.join(HERE, "articles"); os.makedirs(out_dir, exist_ok=True)
    body.save(os.path.join(out_dir, f"{slug}_body.png"))
    W = body.width
    parts = [stamp.fit_width(stamp.make_header(a.date), W), body,
             stamp.fit_width(Image.open(stamp.FOOTER).convert("RGB"), W)]
    out = Image.new("RGB", (W, sum(i.height for i in parts)), "white")
    y = 0
    for i in parts:
        out.paste(i, (0, y)); y += i.height
    path = a.output or os.path.join(out_dir, f"{date.today().isoformat()}_{slug}.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
