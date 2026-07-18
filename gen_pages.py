import json, re, os

# Load scraped movies
src = open("movies.js", encoding="utf-8").read()
m = re.search(r"window.SCRAPER_MOVIES = (.*);", src, re.S)
MOVIES = json.loads(m.group(1))

# Category -> human title + keywords
CATS = {
    "trending":   ("Trending Movies", "trending movies, new movies 2026"),
    "bollywood":  ("Bollywood Movies", "bollywood movies, hindi movies, bollywood hd"),
    "south":      ("South Hindi Dubbed", "south hindi dubbed movies, telugu dubbed"),
    "tollywood":  ("Tollywood Movies", "tollywood movies, telugu movies"),
    "hollywood":  ("Hollywood Movies", "hollywood movies, english movies hd"),
    "bangla":     ("Bangla Dubbed", "bangla dubbed movies, bangladeshi movies"),
    "action":     ("Action Movies", "action movies, fight movies"),
    "comedy":     ("Comedy Movies", "comedy movies, funny movies"),
    "crime":      ("Crime Movies", "crime movies, thriller crime"),
    "drama":      ("Drama Movies", "drama movies"),
    "horror":     ("Horror Movies", "horror movies, scary movies"),
    "romance":    ("Romance Movies", "romance movies, love stories"),
    "scifi":      ("Sci-Fi Movies", "sci fi movies, futuristic movies"),
    "thriller":   ("Thriller Movies", "thriller movies, suspense"),
    "fantasy":    ("Fantasy Movies", "fantasy movies, magic movies"),
    "mystery":    ("Mystery Movies", "mystery movies"),
    "adventure":  ("Adventure Movies", "adventure movies"),
    "animation":  ("Animation Movies", "animated movies, cartoon movies"),
    "family":     ("Family Movies", "family movies"),
    "history":    ("History Movies", "historical movies"),
    "war":        ("War Movies", "war movies"),
    "music":      ("Music Movies", "musical movies"),
    "anime":      ("Anime & Series", "anime, web series"),
    "new":        ("New Releases", "new movie releases 2026"),
}

os.makedirs("category", exist_ok=True)

def card(m):
    poster = m.get("poster","")
    title = m.get("title","").replace('"',"")
    year = m.get("year","")
    rate = m.get("rating","")
    return f'''<a class="card" href="https://jaz-entertainment.netlify.app/" target="_blank">
      <img src="{poster}" alt="{title}" loading="lazy"/>
      <div class="cinfo"><b>{title}</b><small>★ {rate} • {year}</small></div>
    </a>'''

for key,(title,kw) in CATS.items():
    items = [x for x in MOVIES if x.get("_sec")==key][:24]
    if not items: continue
    cards = "\n".join(card(x) for x in items)
    html = f'''<!doctype html><html lang="bn"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Watch {title} Free HD — KIKSLAB STUDIO</title>
<meta name="description" content="Download & watch {title} free in HD. {kw}. Via Telegram @KiksLabMovies.">
<meta name="keywords" content="{kw}, free movie download, hd movie">
<meta property="og:title" content="Watch {title} Free — KIKSLAB">
<meta property="og:type" content="website">
<link rel="canonical" href="https://jaz-entertainment.netlify.app/category/{key}.html">
<style>body{{font-family:Arial;background:#0b0b0b;color:#fff;margin:0}}header{{display:flex;justify-content:space-between;padding:14px 4%;background:#000}}a.logo{{color:#e50914;font-weight:900;font-size:22px;text-decoration:none}}a.tg{{background:#2aabee;color:#fff;padding:8px 14px;border-radius:20px;text-decoration:none}}h1{{padding:20px 4% 0;font-size:26px}}p.sub{{padding:0 4%;color:#aaa}}div.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px;padding:20px 4%}}a.card{{background:#1a1a1a;border-radius:6px;overflow:hidden;text-decoration:none;color:#fff}}a.card img{{width:100%;height:230px;object-fit:cover;display:block}}a.card .cinfo{{padding:8px}}a.card small{{color:#aaa}}footer{{padding:30px 4%;color:#777;text-align:center}}</style>
<script src='https://pub.increaserev.com/pub/increaserev.php?site=9489668&id=monetag' type='text/javascript'></script>
<script src='https://effectivecpmnetwork.com/h4z1tyq1?key=adsterra' type='text/javascript'></script>
</head><body>
<header><a href="https://jaz-entertainment.netlify.app/" class="logo">KIKSLAB</a>
<a href="https://t.me/KiksLabMovies" class="tg">📩 Telegram</a></header>
<h1>{title} — Free HD</h1>
<p class="sub">Watch & download {title.lower()} free. Join Telegram for links.</p>
<div class="grid">{cards}</div>
<footer>Movie data via TMDB. Download links on Telegram @KiksLabMovies. For entertainment only.</footer>
</body></html>'''
    open(f"category/{key}.html","w",encoding="utf-8").write(html)

print(f"✅ {len([k for k in CATS if any(x.get('_sec')==k for x in MOVIES)])} category pages generated")
