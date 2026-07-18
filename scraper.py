import urllib.request, json, datetime

TMDB = "https://api.themoviedb.org/3"
KEY = "029922d0ce729264a5fcd6f7403ec732"
TG = "https://t.me/KiksLabMovies"
YT = "https://www.googleapis.com/youtube/v3/search"  # no key -> we use TMDB videos instead

def api(path):
    try:
        with urllib.request.urlopen(f"{TMDB}{path}&api_key={KEY}", timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print("ERR", path, e); return {}

# Better than mlfbd: multi-language + genre + trailer
G = lambda gid: f"/discover/movie?api_key={KEY}&with_genres={gid}&sort_by=popularity.desc"
SECTIONS = {
    "trending":   f"/trending/movie/day?api_key={KEY}",
    "bollywood":  f"/discover/movie?api_key={KEY}&region=IN&with_original_language=hi&sort_by=popularity.desc",
    "south":      f"/discover/movie?api_key={KEY}&region=IN&with_original_language=ta&sort_by=popularity.desc",
    "tollywood":  f"/discover/movie?api_key={KEY}&region=IN&with_original_language=te&sort_by=popularity.desc",
    "hollywood":  f"/movie/popular?api_key={KEY}",
    "bangla":     f"/discover/movie?api_key={KEY}&with_original_language=bn&sort_by=popularity.desc",
    "anime":      f"/discover/movie?api_key={KEY}&with_genres=16&with_origin_country=JP&sort_by=popularity.desc",
    "new":        f"/movie/now_playing?api_key={KEY}",
    "action":     G(28),
    "comedy":     G(35),
    "crime":      G(80),
    "drama":      G(18),
    "horror":     G(27),
    "romance":    G(10749),
    "scifi":      G(878),
    "thriller":   G(53),
    "fantasy":    G(14),
    "mystery":    G(9648),
    "adventure":  G(12),
    "animation":  G(16),
    "family":     G(10751),
    "history":    G(36),
    "war":        G(10752),
    "music":      G(10402),
    "documentary":G(99),
}

def trailer(mid):
    v = api(f"/movie/{mid}/videos?api_key={KEY}").get("results", [])
    for x in v:
        if x.get("site")=="YouTube" and x.get("type") in ("Trailer","Teaser"):
            return f"https://youtu.be/{x['key']}"
    return ""

def norm(m):
    mid = m.get("id")
    return {
        "id": mid,
        "title": m.get("title") or m.get("original_title",""),
        "poster": ("https://image.tmdb.org/t/p/w500"+m["poster_path"]) if m.get("poster_path") else "",
        "rating": m.get("vote_average",0),
        "year": (m.get("release_date","")[:4]),
        "overview": m.get("overview",""),
        "link": TG,
        "trailer": trailer(mid),
        "tmdb_id": mid,
    }

all_m = {}
for name, path in SECTIONS.items():
    for m in api(path).get("results", [])[:30]:
        nm = norm(m)
        nm["_sec"] = name
        all_m[nm["title"]] = nm

gmap = {g["id"]: g["name"] for g in api(f"/genre/movie/list?api_key={KEY}").get("genres",[])}
for t, m in all_m.items():
    m["genres"] = gmap

LIST = list(all_m.values())
links = {m["title"]: TG for m in LIST}
out = f"window.SCRAPER_LINKS = {json.dumps(links, ensure_ascii=False)};\n"
out += f"window.SCRAPER_MOVIES = {json.dumps(LIST, ensure_ascii=False)};\n"
with open("movies.js","w",encoding="utf-8") as f:
    f.write(out)
print(f"✅ {len(LIST)} movies (Bollywood/South/Tollywood/Hollywood/Anime) + trailers @ {datetime.date.today()}")
