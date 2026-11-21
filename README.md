# Parody Pulse assets

Brand images for Parody Pulse articles. Public repo. Use the raw URLs below.

| File | Size (px) | Use | Raw URL |
|---|---|---|---|
| header/ParodyPulse_Header_2026-11.png | 1080x161 | Article header, "November 2026" date baked in | https://raw.githubusercontent.com/Awarently/parody-pulse-assets/main/header/ParodyPulse_Header_2026-11.png |
| header/ParodyPulse_Header_Base_NoDate.png | 1080x161 | Header with the date removed. Draw the date text on it for a new month | https://raw.githubusercontent.com/Awarently/parody-pulse-assets/main/header/ParodyPulse_Header_Base_NoDate.png |
| footer/ParodyPulse_Footer.png | 1084x78 | Article footer, "@ParodyPulse" bar. No date | https://raw.githubusercontent.com/Awarently/parody-pulse-assets/main/footer/ParodyPulse_Footer.png |
| masthead/ParodyPulse_Masthead_Banner.png | 1122x250 | Standalone banner, no date | https://raw.githubusercontent.com/Awarently/parody-pulse-assets/main/masthead/ParodyPulse_Masthead_Banner.png |

## Layout of an article
Header on top, then headline, subhead, image and body text, then footer. Keep header and footer at full article width.

## Date on the header
Use the NoDate base file. Draw the month and year as white serif text (Libre Baskerville or Georgia), about 20 px, right-aligned at x=1068, baseline y=26, with a faint dark shadow. Name the new file ParodyPulse_Header_YYYY-MM.png.

## Colors
Navy background (about #01142D), red (#E8102E range), white text.

## Automation: stamp.py
Adds the header (current month filled in) and the footer to an article body image.

    pip install pillow
    python stamp.py body.png                       # writes body_final.png
    python stamp.py body.png --date "December 2026" -o article.png

The body image is the article without header and footer (headline, subhead, photo, text). Header and footer are scaled to its width. The date is shrunk automatically if it is too long.

## Using it from an LLM
- Claude Code or any coding agent: clone this repo and run stamp.py. No pasting.
- Chat tools without code execution: give the raw URLs above and attach the body image. They cannot run the script.

## One-command article
`make_article.py` generates the body with an image API (OpenAI by default, Gemini with `--provider gemini`), then adds the header and footer. Needs an API key in `.env` (`OPENAI_API_KEY=...`). `CLAUDE.md`, `AGENTS.md` and `GEMINI.md` tell Claude Code, Codex and Gemini CLI how to run it when asked for a Parody Pulse article.
