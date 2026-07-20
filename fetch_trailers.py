#!/usr/bin/env python3
"""Fetch trailers for existing movies in movies.js (one-time update)"""
import json, re, urllib.request, sys, time

TMDB = "https://api.themoviedb.org/3"
KEY = "029922d0ce729264a5fcd6f7403ec732"
MOVIES_FILE = "movies.js"

def api(path):
    try:
        with urllib.request.urlopen(f"{TMDB}{path}&api_key={KEY}", timeout=15) as r:
            return json.load(r)
    except: return {}

# Load movies — same regex as telegram_bot.py
src = open(MOVIES_FILE, encoding="utf-8").read()
movies = json.loads(re.search(r"window\.SCRAPER_MOVIES = (.*?\]);", src, re.S).group(1))
print(f"Loaded {len(movies)} entries")

# Unique tmdb_ids that need trailers
unique_ids = set()
for m in movies:
    if not m.get("trailer") and m.get("tmdb_id"):
        unique_ids.add(m["tmdb_id"])
print(f"Unique movies needing trailers: {len(unique_ids)}")

# Fetch trailers (~200 per run to stay fast)
MAX = min(100, len(unique_ids))
trailer_cache = {}
count = 0
for mid in sorted(unique_ids):
    if count >= MAX:
        break
    try:
        data = api(f"/movie/{mid}/videos?language=en-US")
        for v in data.get("results", []):
            if v.get("type") == "Trailer" and v.get("site") == "YouTube":
                trailer_cache[mid] = f"https://www.youtube.com/watch?v={v['key']}"
                break
    except: pass
    time.sleep(0.25)
    count += 1
    if count % 25 == 0:
        # Save progress every 25
        for m in movies:
            mid = m.get("tmdb_id")
            if mid in trailer_cache:
                m["trailer"] = trailer_cache[mid]
        links = {m["title"]: m.get("link", "https://t.me/KiksLabMovies") for m in movies}
        out = f"window.SCRAPER_LINKS = {json.dumps(links, ensure_ascii=False)};\n"
        out += f"window.SCRAPER_MOVIES = {json.dumps(movies, ensure_ascii=False)};\n"
        with open(MOVIES_FILE, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"  ✓ {count}/{MAX} — {len(trailer_cache)} trailers (saved)")

print(f"Trailers fetched: {len(trailer_cache)}")

# Update movie entries
updated = 0
for m in movies:
    mid = m.get("tmdb_id")
    if mid in trailer_cache:
        m["trailer"] = trailer_cache[mid]
        updated += 1

# Save back
links = {m["title"]: m.get("link", "https://t.me/KiksLabMovies") for m in movies}
out = f"window.SCRAPER_LINKS = {json.dumps(links, ensure_ascii=False)};\n"
out += f"window.SCRAPER_MOVIES = {json.dumps(movies, ensure_ascii=False)};\n"
with open(MOVIES_FILE, "w", encoding="utf-8") as f:
    f.write(out)

trailer_count = len([m for m in movies if m.get("trailer")])
print(f"\n✅ movies.js updated — {trailer_count}/{len(movies)} entries have trailers")
