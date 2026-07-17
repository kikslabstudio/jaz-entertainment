import urllib.request, json, os, datetime

TMDB = "https://api.themoviedb.org/3"
KEY = "029922d0ce729264a5fcd6f7403ec732"
TG = "https://t.me/KiksLabMovies"

def api(path):
    try:
        with urllib.request.urlopen(f"{TMDB}{path}&api_key={KEY}", timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print("ERR", path, e)
        return {}

# Bollywood/South + Hollywood mix (mlfbd-style categories)
SECTIONS = {
    "trending":   f"/trending/movie/day?api_key={KEY}",
    "bollywood":  f"/movie/now_playing?api_key={KEY}&region=IN&with_original_language=hi",
    "south":      f"/discover/movie?api_key={KEY}&region=IN&with_genres=18&sort_by=popularity.desc&with_original_language=ta",
    "hollywood":  f"/movie/popular?api_key={KEY}",
    "anime":      f"/discover/movie?api_key={KEY}&with_genres=16&with_origin_country=JP&sort_by=popularity.desc",
    "new":        f"/movie/now_playing?api_key={KEY}",
}

def norm(m):
    return {
        "id": m.get("id"),
        "title": m.get("title") or m.get("original_title",""),
        "poster": ("https://image.tmdb.org/t/p/w500"+m["poster_path"]) if m.get("poster_path") else "",
        "rating": m.get("vote_average",0),
        "year": (m.get("release_date","")[:4]),
        "overview": m.get("overview",""),
        "link": TG,
    }

all_m = {}
for name, path in SECTIONS.items():
    data = api(path)
    for m in data.get("results", [])[:25]:
        nm = norm(m)
        nm["_sec"] = name   # tag for frontend filter
        all_m[nm["title"]] = nm  # dedupe by title

# genre map
gmap = {g["id"]: g["name"] for g in api(f"/genre/movie/list?api_key={KEY}").get("genres",[])}
for t, m in all_m.items():
    m["genres"] = gmap

LIST = list(all_m.values())
# SCRAPER_LINKS = Telegram fallback (real host later)
links = {m["title"]: TG for m in LIST}
out = f"window.SCRAPER_LINKS = {json.dumps(links, ensure_ascii=False)};\n"
out += f"window.SCRAPER_MOVIES = {json.dumps(LIST, ensure_ascii=False)};\n"
with open("movies.js","w",encoding="utf-8") as f:
    f.write(out)
print(f"✅ {len(LIST)} movies written to movies.js ({datetime.date.today()})")
