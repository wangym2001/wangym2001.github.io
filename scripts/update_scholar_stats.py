#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


SCHOLAR_ID = "2C1VDq8AAAAJ"
PROFILE_URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en"
OUTPUT = Path(__file__).resolve().parents[1] / "scholar-stats.json"


def parse_number(value: str) -> int:
    return int(value.replace(",", "").strip())


response = requests.get(
    PROFILE_URL,
    headers={
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "Chrome/124.0 Safari/537.36"
        )
    },
    timeout=30,
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
values = [cell.get_text(strip=True) for cell in soup.select("td.gsc_rsb_std")]
if len(values) < 4:
    raise RuntimeError("Google Scholar metrics were not found; the response may be a CAPTCHA page.")

stats = {
    "citations": parse_number(values[0]),
    "h_index": parse_number(values[2]),
    "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
}
OUTPUT.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
print(json.dumps(stats))