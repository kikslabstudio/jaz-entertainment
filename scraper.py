import urllib.request, json, datetime, time

TMDB = "https://api.themoviedb.org/3"
KEY = "029922d0ce729264a5fcd6f7403ec732"
TG = "https://t.me/KiksLabMovies"

# trailer cache to avoid duplicate API calls
_trailer_cache = {}

def trailer(mid):
    """Fetch YouTube trailer URL from TMDB videos endpoint"""
    if mid in _trailer_cache:
        return _trailer_cache[mid]
    try:
        data = api(f"/movie/{mid}/videos?language=en-US")
        for v in data.get("results", []):
            if v.get("type") == "Trailer" and v.get("site") == "YouTube":
                url = f"https://www.youtube.com/watch?v={v['key']}"
                _trailer_cache[mid] = url
                return url
        _trailer_cache[mid] = ""
        return ""
    except:
        _trailer_cache[mid] = ""
        return ""

def api(path):
    try:
        with urllib.request.urlopen(f"{TMDB}{path}&api_key={KEY}", timeout=20) as r:
            return json.load(r)
    except Exception as e:
        print("ERR", path, e); return {}

PAGES = 15  # per section — gives ~300 movies per popular category
PAGES_SMALL = 8  # for niche sections

G = lambda gid: f"/discover/movie?with_genres={gid}&sort_by=popularity.desc"
GS = lambda gid: f"/discover/movie?with_genres={gid}&sort_by=vote_count.desc"

SECTIONS = {
    "trending":   [f"/trending/movie/day?page={p}" for p in range(1,PAGES+1)],
    "new":        [f"/trending/movie/week?page={p}" for p in range(1,PAGES+1)],
    "popular":    [f"/movie/popular?page={p}" for p in range(1,PAGES+1)],
    "top_rated":  [f"/movie/top_rated?page={p}" for p in range(1,PAGES+1)],
    "now_playing":[f"/movie/now_playing?page={p}" for p in range(1,PAGES_SMALL+1)],
    "upcoming":   [f"/movie/upcoming?page={p}" for p in range(1,PAGES_SMALL+1)],
    "bollywood":  [f"/discover/movie?region=IN&with_original_language=hi&sort_by=popularity.desc&page={p}" for p in range(1,PAGES+1)],
    "south":      [f"/discover/movie?region=IN&with_original_language=ta&sort_by=popularity.desc&page={p}" for p in range(1,PAGES+1)],
    "tollywood":  [f"/discover/movie?region=IN&with_original_language=te&sort_by=popularity.desc&page={p}" for p in range(1,PAGES+1)],
    "hollywood":  [f"/discover/movie?with_original_language=en&sort_by=popularity.desc&page={p}" for p in range(1,PAGES+1)],
    "bangla":     [f"/discover/movie?with_original_language=bn&sort_by=popularity.desc&page={p}" for p in range(1,PAGES_SMALL+1)],
    "anime":      [f"/discover/movie?with_genres=16&with_origin_country=JP&sort_by=popularity.desc&page={p}" for p in range(1,PAGES+1)],
    "action":     [G(28) + f"&page={p}" for p in range(1,PAGES+1)],
    "comedy":     [G(35) + f"&page={p}" for p in range(1,PAGES+1)],
    "crime":      [G(80) + f"&page={p}" for p in range(1,PAGES+1)],
    "drama":      [G(18) + f"&page={p}" for p in range(1,PAGES+1)],
    "horror":     [G(27) + f"&page={p}" for p in range(1,PAGES+1)],
    "romance":    [G(10749) + f"&page={p}" for p in range(1,PAGES+1)],
    "scifi":      [G(878) + f"&page={p}" for p in range(1,PAGES+1)],
    "thriller":   [G(53) + f"&page={p}" for p in range(1,PAGES+1)],
    "fantasy":    [G(14) + f"&page={p}" for p in range(1,PAGES+1)],
    "mystery":    [G(9648) + f"&page={p}" for p in range(1,PAGES+1)],
    "adventure":  [G(12) + f"&page={p}" for p in range(1,PAGES+1)],
    "animation":  [G(16) + f"&page={p}" for p in range(1,PAGES+1)],
    "family":     [G(10751) + f"&page={p}" for p in range(1,PAGES+1)],
    "history":    [G(36) + f"&page={p}" for p in range(1,PAGES_SMALL+1)],
    "war":        [G(10752) + f"&page={p}" for p in range(1,PAGES_SMALL+1)],
    "music":      [G(10402) + f"&page={p}" for p in range(1,PAGES_SMALL+1)],
    "documentary":[G(99) + f"&page={p}" for p in range(1,PAGES_SMALL+1)],
    "western":    [G(37) + f"&page={p}" for p in range(1,PAGES_SMALL+1)],
    "tv_movie":   [G(10770) + f"&page={p}" for p in range(1,PAGES_SMALL+1)],
    "korean":     [f"/discover/movie?with_original_language=ko&sort_by=popularity.desc&page={p}" for p in range(1,PAGES_SMALL+1)],
    "japanese":   [f"/discover/movie?with_original_language=ja&sort_by=popularity.desc&page={p}" for p in range(1,PAGES_SMALL+1)],
    "chinese":    [f"/discover/movie?with_original_language=zh&sort_by=popularity.desc&page={p}" for p in range(1,PAGES_SMALL+1)],
    "russian":    [f"/discover/movie?with_original_language=ru&sort_by=popularity.desc&page={p}" for p in range(1,PAGES_SMALL+1)],
}

def norm(m, sec):
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
        "_sec": sec,
    }

LIST = []
seen = set()
total_secs = len(SECTIONS)

for i, (name, paths) in enumerate(SECTIONS.items(), 1):
    for path in paths:
        data = api(path)
        results = data.get("results", [])
        for m in results:
            nm = norm(m, name)
            # dedupe by tmdb_id+section (allow same movie in different categories)
            key = f"{nm['tmdb_id']}_{name}"
            if key not in seen:
                seen.add(key)
                LIST.append(nm)
        time.sleep(0.15)  # respect TMDB rate limits
    print(f"  [{i}/{total_secs}] {name}: {len([x for x in LIST if x['_sec']==name])} movies")

links = {m["title"]: TG for m in LIST}
out = f"window.SCRAPER_LINKS = {json.dumps(links, ensure_ascii=False)};\n"
out += f"window.SCRAPER_MOVIES = {json.dumps(LIST, ensure_ascii=False)};\n"
with open("movies.js","w",encoding="utf-8") as f:
    f.write(out)

# Count unique movies
unique = set(m["tmdb_id"] for m in LIST)
print(f"\n✅ {len(LIST)} entries, {len(unique)} unique movies @ {datetime.date.today()}")
