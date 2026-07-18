#!/usr/bin/env python3
"""
KIKSLAB Telegram Bot — auto-posts new movies to @KiksLabMovies channel
Run:  python telegram_bot.py            # posts up to N new movies from movies.js
       python telegram_bot.py --all     # post all (first run / backfill)
Needs: pip install python-telegram-bot
"""
import os, sys, json, re, asyncio
from telegram import Bot

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN") or "8821668549:AAHdwubrLTKF1ZsRx46Z9oGpdHyczcsH3Ak"  # @KikslabMoviesBot
CHANNEL   = "@KiksLabMovies"
SITE      = "https://jaz-entertainment.netlify.app"
STATE_FILE = "posted.json"   # remembers which movies already posted

def load_movies():
    src = open("movies.js", encoding="utf-8").read()
    arr = json.loads(re.search(r"window.SCRAPER_MOVIES = (.*);", src, re.S).group(1))
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
    rate = m.get("rating","")
    sec = m.get("_sec","").upper()
    poster = m.get("poster","")
    text = (f"🎬 <b>{title}</b> ({year})\n"
            f"⭐ Rating: {rate}\n"
            f"📂 Category: {sec}\n\n"
            f"▶ Watch / Download: {SITE}/\n"
            f"📩 Join: https://t.me/KiksLabMovies")
    return text, poster

async def post_new(limit=5, all_mode=False):
    movies = load_movies()
    posted = set() if all_mode else load_posted()
    bot = Bot(BOT_TOKEN)
    count = 0
    # post newest-first
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
        except Exception as e:
            print("ERR posting", m.get("title"), e)
            break
    save_posted(posted)
    print(f"✅ Posted {count} movie(s) to {CHANNEL}")

if __name__ == "__main__":
    all_mode = "--all" in sys.argv
    lim = 5
    for a in sys.argv[1:]:
        if a.isdigit(): lim = int(a)
    asyncio.run(post_new(limit=lim, all_mode=all_mode))
