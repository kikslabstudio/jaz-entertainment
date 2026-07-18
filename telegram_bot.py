#!/usr/bin/env python3
"""
KIKSLAB Telegram Bot
  python telegram_bot.py              → post 5 new (unposted) movies
  python telegram_bot.py 10           → post 10 new movies
  python telegram_bot.py --random 10  → post 10 random movies (daily use)
  python telegram_bot.py --all        → backfill all movies
"""
import os, sys, json, re, asyncio, random
from telegram import Bot

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN") or "8821668549:AAHdwubrLTKF1ZsRx46Z9oGpdHyczcsH3Ak"
CHANNEL   = "@KiksLabMovies"
SITE      = "https://jaz-entertainment.netlify.app"
STATE_FILE = "posted.json"

def load_movies():
    src = open("movies.js", encoding="utf-8").read()
    arr = json.loads(re.search(r"window\.SCRAPER_MOVIES = (.*?\]);", src, re.S).group(1))
    return arr

def load_posted():
    if os.path.exists(STATE_FILE):
        return set(json.load(open(STATE_FILE, encoding="utf-8")))
    return set()

def save_posted(s):
    json.dump(list(s), open(STATE_FILE, "w", encoding="utf-8"))

def msg_for(m):
    title = m.get("title","")
    year = m.get("year","")
    rate = m.get("rating",0)
    sec = m.get("_sec","").upper()
    poster = m.get("poster","")
    cat_emoji = {
        "TRENDING":"🔥","NEW":"🆕","POPULAR":"⭐","TOP_RATED":"🏆",
        "BOLLYWOOD":"🇮🇳","SOUTH":"🌏","TOLLYWOOD":"🔥","HOLLYWOOD":"🎬",
        "BANGLA":"🇧🇩","ACTION":"💥","COMEDY":"😂","DRAMA":"🎭",
        "HORROR":"👻","ROMANCE":"💕","SCIFI":"🚀","THRILLER":"😱",
        "ANIME":"🌸","FANTASY":"🧙","FAMILY":"👨‍👩‍👧","ANIMATION":"🎨",
    }
    emoji = cat_emoji.get(sec,"🎬")
    text = (
        f"{emoji} <b>{title}</b> ({year})\n"
        f"⭐ {rate:.1f}  •  {sec}\n\n"
        f"▶ <a href='{SITE}/'>Watch / Download HD</a>\n"
        f"📩 <a href='https://t.me/KiksLabMovies'>Join @KiksLabMovies</a>"
    )
    return text, poster

async def post_new(limit=5, all_mode=False):
    movies = load_movies()
    posted = set() if all_mode else load_posted()
    bot = Bot(BOT_TOKEN)
    count = 0
    for m in reversed(movies):
        key = f"{m.get('tmdb_id')}:{m.get('_sec')}"
        if key in posted:
            continue
        text, poster = msg_for(m)
        try:
            if poster:
                await bot.send_photo(chat_id=CHANNEL, photo=poster, caption=text, parse_mode="HTML")
            else:
                await bot.send_message(chat_id=CHANNEL, text=text, parse_mode="HTML")
            posted.add(key)
            count += 1
            if not all_mode and count >= limit:
                break
            await asyncio.sleep(0.5)  # rate limit
        except Exception as e:
            print("ERR", m.get("title"), e)
            break
    save_posted(posted)
    print(f"✅ Posted {count} new movie(s)")

async def post_random(limit=10):
    movies = load_movies()
    bot = Bot(BOT_TOKEN)
    # deduplicate by tmdb_id so same movie doesn't post twice
    seen_ids = set()
    unique = []
    for m in movies:
        tid = m.get("tmdb_id")
        if tid not in seen_ids:
            seen_ids.add(tid)
            unique.append(m)
    random.shuffle(unique)
    count = 0
    for m in unique[:limit]:
        text, poster = msg_for(m)
        try:
            if poster:
                await bot.send_photo(chat_id=CHANNEL, photo=poster, caption=text, parse_mode="HTML")
            else:
                await bot.send_message(chat_id=CHANNEL, text=text, parse_mode="HTML")
            count += 1
            await asyncio.sleep(1.5)  # avoid flood
        except Exception as e:
            print("ERR", m.get("title"), e)
    print(f"✅ Posted {count} random movie(s) to {CHANNEL}")

if __name__ == "__main__":
    if "--random" in sys.argv:
        idx = sys.argv.index("--random")
        lim = int(sys.argv[idx+1]) if idx+1 < len(sys.argv) and sys.argv[idx+1].isdigit() else 10
        asyncio.run(post_random(limit=lim))
    else:
        all_mode = "--all" in sys.argv
        lim = 5
        for a in sys.argv[1:]:
            if a.isdigit(): lim = int(a)
        asyncio.run(post_new(limit=lim, all_mode=all_mode))
