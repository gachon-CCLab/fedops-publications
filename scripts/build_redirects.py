"""Build dependency-free static redirects for the former publication URLs."""

from html import escape
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
DATA = json.loads((ROOT / "redirects.json").read_text(encoding="utf-8"))
BASE = DATA["canonical_base"].rstrip("/")


def write_redirect(path: Path, destination: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_url = escape(destination, quote=True)
    js_url = json.dumps(destination).replace("<", "\\u003c")
    path.write_text(
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">\n'
        f'<meta http-equiv="refresh" content="0; url={safe_url}">\n'
        f'<link rel="canonical" href="{safe_url}">\n'
        '<title>FedOps content has moved</title></head><body>\n'
        f'<p>This page has moved to <a href="{safe_url}">{safe_url}</a>.</p>\n'
        f'<script>location.replace({js_url} + location.search + location.hash);</script>\n'
        '</body></html>\n',
        encoding="utf-8",
    )


if not SITE.resolve().is_relative_to(ROOT.resolve()) or SITE.resolve() == ROOT.resolve():
    raise ValueError("Refusing to remove a build directory outside this repository")
if SITE.exists():
    shutil.rmtree(SITE)
SITE.mkdir()
(SITE / ".nojekyll").touch()
write_redirect(SITE / "index.html", f"{BASE}/")

for section in ("blog", "news"):
    write_redirect(SITE / section / "index.html", f"{BASE}/{section}/")
    slugs = DATA[section]
    if len(slugs) != len(set(slugs)):
        raise ValueError(f"Duplicate {section} redirects")
    for slug in slugs:
        if not re.fullmatch(r"[a-z0-9-]+", slug):
            raise ValueError(f"Unsafe slug: {slug}")
        write_redirect(SITE / section / slug / "index.html", f"{BASE}/{section}/{slug}/")

images = ROOT / "assets" / "blog"
if images.is_dir():
    shutil.copytree(images, SITE / "assets" / "blog")

print(f"Generated {sum(len(DATA[section]) for section in ('blog', 'news')) + 3} redirects")
