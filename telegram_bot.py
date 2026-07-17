#!/usr/bin/env python3
"""
KIKSLAB Telegram Bot — broadcast + DM helper
Run:  python telegram_bot.py
Needs: pip install python-telegram-bot
"""
import asyncio
from telegram import Bot

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"   # from @BotFather
CHANNEL   = "@KiksLabMovies"               # public channel
LINK_TEXT = ("🎬 Free movie link ready!\n"
             "👉 https://t.me/KiksLabMovies\n"
             "Daily HD movies, no spam. 🔥")

async def broadcast():
    bot = Bot(BOT_TOKEN)
    await bot.send_message(chat_id=CHANNEL, text=LINK_TEXT)
    print("✅ Broadcasted to channel.")

async def dm(user_id):
    bot = Bot(BOT_TOKEN)
    await bot.send_message(chat_id=user_id, text=LINK_TEXT)
    print(f"✅ DM sent to {user_id}")

if __name__ == "__main__":
    print("1) Broadcast to channel")
    print("2) DM a user (enter user_id)")
    ch = input("Choose: ").strip()
    if ch == "1":
        asyncio.run(broadcast())
    elif ch == "2":
        uid = input("User ID: ").strip()
        asyncio.run(dm(uid))
