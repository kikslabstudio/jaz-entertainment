============================================================
KIKSLAB BRIDGE — DEPLOY + RUN GUIDE v2
============================================================

FOLDER: C:\Users\Md Rajib Hasan\kikslab-bridge\
  index.html        → professional movie hub (ads + CPA + grid)
  movies.js         → (create) your scraper output goes here
  TELEGRAM_BOT.txt  → bot code + setup
  SCRAPER_HOOK.txt  → how scraper plugs in
  AD_CODES.txt      → ad network reference
  POST_CALENDAR.txt → 13-day FB plan
  README.txt        → this file

------------------------------------------------------------
1) DEPLOY TO NETLIFY (5 min)
------------------------------------------------------------
Easiest — drag & drop:
  1. https://app.netlify.com/drop
  2. Drag the whole "kikslab-bridge" folder
  3. Get URL: https://xxx.netlify.app

CLI (if logged in):
  cd "C:\Users\Md Rajib Hasan\kikslab-bridge"
  netlify deploy --prod --dir .

------------------------------------------------------------
2) TELEGRAM SETUP (you do last, as planned)
------------------------------------------------------------
  a) @BotFather -> /newbot -> get BOT_TOKEN
  b) @userinfobot -> get your CHAT_ID
  c) Create channel @KiksLabMovies (public)
  d) Fill BOT_TOKEN + CHAT_ID in telegram_bot.py
  e) Run: python telegram_bot.py  (broadcasts link to channel)
  f) For each FB comment, reply with t.me/KiksLabMovies (manual or auto)

------------------------------------------------------------
3) SCRAPER (you build, hook ready)
------------------------------------------------------------
  - Write scraper -> outputs movies.js (format in SCRAPER_HOOK.txt)
  - Load <script src="movies.js"> in index.html
  - Redeploy to Netlify
  - Keep dl = Telegram link (NOT direct pirated file)

------------------------------------------------------------
4) AD LINKS (already live in index.html)
------------------------------------------------------------
  Monetag   : omg10.com/4/9489668        (popunder)
  Adsterra  : effectivecpmnetwork...key= (popunder/social bar)
  Advertica : data527.click...           (CPA button "Claim Free Reward")

Verify in dashboard after deploy:
  - Monetag/Adsterra: domain verify for better rate
  - Advertica: check conversions

------------------------------------------------------------
5) DAILY ROUTINE (from POST_CALENDAR.txt)
------------------------------------------------------------
  1. Post 2-3x at 6-9 PM BD
  2. Reply comments with Telegram link (bot or manual)
  3. Check dashboards, log $ in tracker
  4. Reuse best format

GOAL: $300 / 13 days = ~$23/day
Math: 71k × 3% reach × 4% CTR × 3 posts ≈ 255 clicks/day
      + ads (CPM) + 15-25 CPA actions/day
============================================================
