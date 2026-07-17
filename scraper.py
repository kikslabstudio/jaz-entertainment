#!/usr/bin/env python3
"""
KIKSLAB scraper -> movies.js generator
Pulls real movie data from TMDB (your key) and writes window.SCRAPER_LINKS
in the exact format index.html expects.

Default download link = Telegram (@KiksLabMovies).
To use your own host: edit DOWNLOAD_MAP below or point HOST_BASE.

Run:  python scraper.py
Output: movies.js  (drop next to index.html, already referenced)
"""
import json, urllib.request, urllib.parse, time

TMDB_KEY = "029922d0ce729264a5fcd6f7403ec732"
TG = "https://t.me/KiksLabMovies"

# If you have your own download host pattern, set here:
# e.g. HOST_BASE = "https://your-host.com/d/"  -> link = HOST_BASE + slug
HOST_BASE = None

CATEGORIES = {
    "trending": f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_KEY}",
    "popular":  f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_KEY}",
    "new":      f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_KEY}",
    "anime":    f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_KEY}&with_genres=16&with_origin_country=JP&sort_by=popularity.desc",
    "search_sample": f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query=Avengers",
}

def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.load(r).get("results", [])
    except Exception as e:
        print("fetch err:", e)
        return []

def slug(t):
    return urllib.parse.quote(t.lower().replace(" ", "-"))

def main():
    links = {}
    seen = set()
    for cat, url in CATEGORIES.items():
        for m in fetch(url):
            title = m.get("title") or m.get("name")
            if not title or title in seen:
                continue
            seen.add(title)
            # download link: your host if set, else Telegram
            link = (HOST_BASE + slug(title)) if HOST_BASE else TG
            links[title] = link
        time.sleep(0.3)

    out = "window.SCRAPER_LINKS = " + json.dumps(links, ensure_ascii=False, indent=2) + ";\n"
    with open("movies.js", "w", encoding="utf-8") as f:
        f.write(out)
    print(f"✅ movies.js written with {len(links)} movies.")
    print("   Default link = Telegram. Set HOST_BASE to use your own host.")

if __name__ == "__main__":
    main()
