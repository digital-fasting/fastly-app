#!/usr/bin/env python3
"""
Fix public/*.html when pasted from a generator and saved as plain text:
HTML is escaped (e.g. &lt;div&gt;) and wrapped in <p> tags.
Usage: python3 fix-pasted-html.py [privacy|terms]
  privacy -> public/privacy.html, title "Privacy Policy — Fastly"
  terms   -> public/terms.html,   title "Terms and Conditions — Fastly"
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

PAGES = {
    "privacy": ("privacy.html", "Privacy Policy — Fastly"),
    "terms": ("terms.html", "Terms and Conditions — Fastly"),
}


def extract_body_text(html_content: str) -> str:
    """Get inner text from body, stripping wrapper <p>/<span> tags."""
    match = re.search(r"<body[^>]*>(.*)</body>", html_content, re.DOTALL | re.IGNORECASE)
    if not match:
        raise SystemExit("No <body> found in file")
    body = match.group(1)
    body = re.sub(r"<p[^>]*>", "", body)
    body = re.sub(r"</p>", "\n", body)
    body = re.sub(r"<span[^>]*>", "", body)
    body = re.sub(r"</span>", "", body)
    return body


def fix_file(path: Path, title: str) -> None:
    raw = path.read_text(encoding="utf-8")
    inner = extract_body_text(raw)
    unescaped = html.unescape(inner)

    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; line-height: 1.6; color: #333; max-width: 720px; margin: 0 auto; padding: 24px; }}
    h1 {{ font-size: 1.75rem; margin-top: 1.5em; }}
    h2 {{ font-size: 1.25rem; margin-top: 1.25em; }}
    a {{ color: #0094FF; }}
    .subtitle {{ color: #666; font-size: 0.9rem; }}
  </style>
</head>
<body>
""" + unescaped.strip() + "\n</body>\n</html>\n"

    path.write_text(out, encoding="utf-8")
    print(f"Fixed {path} ({len(out)} bytes)")


def main() -> None:
    which = (sys.argv[1:] or ["privacy"])[0].lower()
    if which not in PAGES:
        print(f"Usage: {sys.argv[0]} [privacy|terms]", file=sys.stderr)
        sys.exit(1)
    filename, title = PAGES[which]
    path = PUBLIC / filename
    if not path.exists():
        print(f"Not found: {path}", file=sys.stderr)
        sys.exit(1)
    fix_file(path, title)


if __name__ == "__main__":
    main()
