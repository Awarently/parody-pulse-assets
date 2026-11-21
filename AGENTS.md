# Parody Pulse

Satirical newsletter. This repo holds the brand header, footer and article tooling.

## When the user asks for a Parody Pulse article
Do this without asking about files or scripts:
1. Write the four pieces in Parody Pulse voice (dry, deadpan, plausible-sounding satire; clearly fictional):
   - headline (max about 9 words, fits 2 lines)
   - subhead (one sentence, about 25 words)
   - text (about 60 words, fits 4 lines)
   - scene (one concrete photographic scene description)
2. Run, from the repo root:
   `python make_article.py --headline "..." --subhead "..." --text "..." --scene "..."`
   The standard header (today's month and year) and footer are added automatically. Use `--date "Month YYYY"` only if the user names a date. Use `--provider gemini` only if the user asks for Gemini.
3. Show or send the final PNG from `articles/`. Tell the user the path.

If the command fails because of a missing key, tell the user to put `OPENAI_API_KEY=...` (or `GEMINI_API_KEY=...`) in a `.env` file in the repo root. Never print or commit keys.

If the user supplies their own body image, run `python stamp.py body.png` instead.

## Files
- header/, footer/, masthead/: brand images (see README.md)
- stamp.py: adds header and footer to a body image
- make_article.py: generates the body with an image API, then stamps it
