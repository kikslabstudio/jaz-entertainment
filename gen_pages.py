import json, re, os

# Load scraped movies
src = open("movies.js", encoding="utf-8").read()
m = re.search(r"window.SCRAPER_MOVIES = (.*);", src, re.S)
MOVIES = json.loads(m.group(1))

# Category -> human title + SEO keywords (mlfbd-style keyword stuffing)
CATS = {
    "trending":   ("Trending Movies", "trending movies, new movies 2026, latest movies"),
    "bollywood":  ("Bollywood Movies", "bollywood movies, hindi movies, bollywood hd download, hindi film"),
    "south":      ("South Hindi Dubbed", "south hindi dubbed movies, telugu dubbed, tamil dubbed hindi"),
    "tollywood":  ("Tollywood Movies", "tollywood movies, telugu movies, telugu film"),
    "hollywood":  ("Hollywood Movies", "hollywood movies, english movies hd, hollywood hindi dubbed"),
    "bangla":     ("Bangla Dubbed", "bangla dubbed movies, bangladeshi movies, bd movie"),
    "action":     ("Action Movies", "action movies, fight movies, action thriller"),
    "comedy":     ("Comedy Movies", "comedy movies, funny movies, comedy film"),
    "crime":      ("Crime Movies", "crime movies, crime thriller, gangster movies"),
    "drama":      ("Drama Movies", "drama movies, emotional movies"),
    "horror":     ("Horror Movies", "horror movies, scary movies, haunted movie"),
    "romance":    ("Romance Movies", "romance movies, love story, romantic film"),
    "scifi":      ("Sci-Fi Movies", "sci fi movies, futuristic movies, space movie"),
    "thriller":   ("Thriller Movies", "thriller movies, suspense movie, mystery thriller"),
    "fantasy":    ("Fantasy Movies", "fantasy movies, magic movies, fairy tale"),
    "mystery":    ("Mystery Movies", "mystery movies, detective movie"),
    "adventure":  ("Adventure Movies", "adventure movies, journey film"),
    "animation":  ("Animation Movies", "animated movies, cartoon movies, kids animation"),
    "family":     ("Family Movies", "family movies, kids movie"),
    "history":    ("History Movies", "historical movies, period drama"),
    "war":        ("War Movies", "war movies, battle film, military movie"),
    "music":      ("Music Movies", "musical movies, music film"),
    "anime":      ("Anime & Series", "anime, web series, anime movie"),
    "new":        ("New Releases", "new movie releases 2026, upcoming movies"),
}

SITE = "https://jaz-entertainment.netlify.app"
os.makedirs("category", exist_ok=True)

GENRE_LINKS = "".join(f'<a href="{SITE}/category/{k}.html">{v[0]}</a> | ' for k,v in CATS.items())

def card(m):
    poster = m.get("poster","")
    title = m.get("title","").replace('"',"")
    year = m.get("year","")
    rate = m.get("rating","")
    return f'''<a class="card" href="{SITE}/" target="_blank" rel="noopener">
      <img src="{poster}" alt="{title} {year} full movie hd" loading="lazy"/>
      <div class="cinfo"><b>{title}</b><small>★ {rate} • {year} • HD</small></div>
    </a>'''

for key,(title,kw) in CATS.items():
    items = [x for x in MOVIES if x.get("_sec")==key][:30]
    if not items:
        print(f"SKIP {key} (0 movies)"); continue
    cards = "\n".join(card(x) for x in items)
    # Schema.org JSON-LD for SEO rich results
    ld = json.dumps({
        "@context":"https://schema.org",
        "@type":"CollectionPage",
        "name":f"{title} — Watch Free HD",
        "description":f"Download & watch {title} free in HD. {kw}.",
        "url":f"{SITE}/category/{key}.html",
        "isPartOf":{"@type":"WebSite","name":"KIKSLAB STUDIO","url":SITE},
        "breadcrumb":{"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":SITE},
            {"@type":"ListItem","position":2,"name":title,"item":f"{SITE}/category/{key}.html"}
        ]}
    }, ensure_ascii=False)
    html = f'''<!doctype html><html lang="bn"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Watch {title} Free HD Download — KIKSLAB STUDIO</title>
<meta name="description" content="Download & watch {title} free in HD quality. {kw}. Join Telegram @KiksLabMovies for download links.">
<meta name="keywords" content="{kw}, free movie download, hd movie download, watch online">
<meta property="og:title" content="Watch {title} Free — KIKSLAB">
<meta property="og:description" content="Free HD {title}. Download via Telegram.">
<meta property="og:type" content="website">
<link rel="canonical" href="{SITE}/category/{key}.html">
<script type="application/ld+json">{ld}</script>
<style>body{{font-family:Arial,Roboto,sans-serif;background:#0b0b0b;color:#fff;margin:0}}header{{display:flex;justify-content:space-between;align-items:center;padding:14px 4%;background:#000;position:sticky;top:0;z-index:10}}a.logo{{color:#e50914;font-weight:900;font-size:22px;text-decoration:none}}a.tg{{background:#2aabee;color:#fff;padding:8px 14px;border-radius:20px;text-decoration:none;font-weight:700}}.genres{{padding:10px 4%;background:#111;font-size:13px;line-height:2}}a.genre{{color:#ccc;text-decoration:none;margin-right:4px}}a.genre:hover{{color:#e50914}}h1{{padding:20px 4% 0;font-size:26px;margin:0}}p.sub{{padding:4px 4% 0;color:#aaa}}div.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px;padding:20px 4%}}a.card{{background:#1a1a1a;border-radius:6px;overflow:hidden;text-decoration:none;color:#fff}}a.card img{{width:100%;height:230px;object-fit:cover;display:block}}a.card .cinfo{{padding:8px}}a.card small{{color:#aaa}}footer{{padding:30px 4%;color:#777;text-align:center;border-top:1px solid #222;margin-top:20px}}</style>
<script src='https://pub.increaserev.com/pub/increaserev.php?site=9489668&id=monetag' type='text/javascript'></script>
<script src='https://effectivecpmnetwork.com/h4z1tyq1?key=adsterra' type='text/javascript'></script>
</head><body>
<header><a href="{SITE}/" class="logo">KIKSLAB</a>
<a href="https://t.me/KiksLabMovies" class="tg">📩 Telegram</a></header>
<nav class="genres">{GENRE_LINKS}</nav>
<h1>{title} — Free HD Download</h1>
<p class="sub">Watch & download {title.lower()} free in HD. Click any movie → Telegram for download link.</p>
<div class="grid">{cards}</div>
<footer>Movie data via TMDB. Download links on Telegram @KiksLabMovies. For entertainment only.<br>© KIKSLAB STUDIO</footer>
</body></html>'''
    open(f"category/{key}.html","w",encoding="utf-8").write(html)

cats = [k for k in CATS if any(x.get("_sec")==k for x in MOVIES)]
print(f"✅ {len(cats)} category pages generated (schema.org + internal links)")
