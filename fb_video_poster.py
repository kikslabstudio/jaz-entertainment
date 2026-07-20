#!/usr/bin/env python3
"""
FB Auto Video Poster — Download → Post → Delete cycle
======================================================
Usage:
  python fb_video_poster.py              → post 1 video
  python fb_video_poster.py 5            → post 5 videos
  python fb_video_poster.py --random     → post random movies with trailers
  python fb_video_poster.py --section=bollywood  → only Bollywood trailers

Requirements:
  - yt-dlp (pip install yt-dlp)
  - FB_PAGE_TOKEN environment variable OR edit TOKEN below
"""
import os, sys, json, re, time, subprocess, glob, tempfile, shutil

# ==== CONFIG ====
TOKEN = "EAATuDAFdfY8BSGj5twzq9ycXxNV2nM6oHv9PZANw4zKiPoZAMol5dPgg1JDUvZBKEQNo0XF61m203OxD1ax4xar5eWsVlylGkUnvBEhccoQ4ZAVdLNc0iTHoAGZA2aiwDL9I9KkyDvdEfsin7C7VwsjYxQ4YObBR4q6UliYpRB31XMJ7kNHjyzH5GUzELlYOhmbhSzKmdi2XeE5Q7iRVmhFZB0jIql2s8wGVZASbZCdO"
PAGE_ID = "660998157085984"  # Raina46
SITE = "https://jaz-entertainment.netlify.app"
STATE_FILE = "posted_fb_video.json"
MOVIES_FILE = "movies.js"
TEMP_DIR = os.path.join(tempfile.gettempdir(), "kikslab_fb_videos")
os.makedirs(TEMP_DIR, exist_ok=True)

# ==== HELPERS ====
def load_movies():
    src = open(MOVIES_FILE, encoding="utf-8").read()
    return json.loads(re.search(r"window\.SCRAPER_MOVIES = (.*?\])", src, re.S).group(1))

def load_posted():
    if os.path.exists(STATE_FILE):
        return set(json.load(open(STATE_FILE, encoding="utf-8")))
    return set()

def save_posted(s):
    json.dump(list(s), open(STATE_FILE, "w", encoding="utf-8"))

def download_trailer(m):
    """Download YouTube trailer to temp dir. Returns path or None."""
    url = m.get("trailer", "")
    if not url or "youtube" not in url.lower():
        return None
    title = m.get("title", "unknown")
    safe = re.sub(r'[\\/*?:"<>|]', "", title)[:50]
    out_path = os.path.join(TEMP_DIR, f"{safe}.mp4")
    
    # Skip if already downloaded (shouldn't happen since we clean up)
    if os.path.exists(out_path):
        return out_path
    
    try:
        subprocess.run(
            ["python", "-m", "yt_dlp", "-f", "best[height<=720]", 
             "-o", out_path, "--no-playlist", "--quiet", url],
            timeout=120, check=True,
            capture_output=True
        )
        if os.path.exists(out_path) and os.path.getsize(out_path) > 50000:
            return out_path
    except Exception as e:
        print(f"  ⚠️ Download failed: {e}")
    return None

def post_to_fb(video_path, caption):
    """Upload video to FB page via Graph API. Returns True on success."""
    import urllib.request
    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    
    # Build multipart form
    body = []
    # Caption field
    body.append(f"--{boundary}")
    body.append('Content-Disposition: form-data; name="message"')
    body.append("")
    body.append(caption.encode("utf-8"))
    
    # Video file
    with open(video_path, "rb") as f:
        vid_data = f.read()
    body.append(f"--{boundary}")
    body.append(f'Content-Disposition: form-data; name="source"; filename="trailer.mp4"')
    body.append("Content-Type: video/mp4")
    body.append("")
    body.append(vid_data)
    body.append(f"--{boundary}--")
    
    # Join all parts
    body_data = b"\r\n".join(b if isinstance(b, bytes) else b for b in body)
    
    url = f"https://graph.facebook.com/v22.0/{PAGE_ID}/videos?access_token={TOKEN}"
    req = urllib.request.Request(url, data=body_data)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read())
            if result.get("id"):
                print(f"  ✅ FB post ID: {result['id']}")
                return True
            print(f"  ⚠️ FB response: {result}")
            return False
    except Exception as e:
        print(f"  ❌ FB upload failed: {e}")
        return False

def caption_for(m):
    """Generate FB caption for video post"""
    title = m.get("title", "")
    year = m.get("year", "")
    rate = m.get("rating", 0)
    sec = m.get("_sec", "").upper()
    cat_emoji = {
        "BOLLYWOOD":"🇮🇳","SOUTH":"🌏","TOLLYWOOD":"🔥","HOLLYWOOD":"🎬",
        "BANGLA":"🇧🇩","ACTION":"💥","COMEDY":"😂","HORROR":"👻","ANIME":"🌸",
    }
    emoji = cat_emoji.get(sec, "🎬")
    return (
        f"{emoji} {title} ({year}) ⭐ {rate:.1f}\n\n"
        f"🎬 Watch Full Movie: {SITE}/\n"
        f"📩 Join: t.me/KiksLabMovies\n\n"
        f"#MovieTrailer #NewRelease #KIKSLAB"
    )

def clean_temp(keep_path=None):
    """Delete all temp videos except keep_path"""
    for f in glob.glob(os.path.join(TEMP_DIR, "*.mp4")):
        if f != keep_path:
            try: os.remove(f)
            except: pass

# ==== MAIN ====
def main():
    if TOKEN == "YOUR_TOKEN_HERE":
        print("❌ FB_PAGE_TOKEN not set!")
        print("   Either: export FB_PAGE_TOKEN=your_token_here")
        print("   Or edit TOKEN in fb_video_poster.py")
        sys.exit(1)
    
    movies = load_movies()
    posted = load_posted()
    
    # Filter: only movies with trailers
    with_trailer = [m for m in movies if m.get("trailer")]
    print(f"📊 Movies with trailers: {len(with_trailer)}/{len(movies)}")
    
    # Section filter
    section = None
    for a in sys.argv[1:]:
        if a.startswith("--section="):
            section = a.split("=", 1)[1].lower()
    if section:
        with_trailer = [m for m in with_trailer if m.get("_sec","") == section]
        print(f"   Filtered by section '{section}': {len(with_trailer)}")
    
    limit = 1
    for a in sys.argv[1:]:
        if a.isdigit(): limit = int(a)
    
    is_random = "--random" in sys.argv
    if is_random:
        import random
        random.shuffle(with_trailer)
    
    count = 0
    for m in with_trailer:
        key = f"fb_video_{m.get('tmdb_id')}"
        if key in posted:
            continue
        
        print(f"\n🎬 {m['title']} ({m.get('year','')})")
        print(f"   Trailer: {m['trailer'][:60]}...")
        
        # Step 1: Download
        print("   ⬇ Downloading...", end=" ", flush=True)
        video_path = download_trailer(m)
        if not video_path:
            print("❌ failed")
            posted.add(key)  # skip this one next time
            save_posted(posted)
            continue
        size_mb = os.path.getsize(video_path) / (1024*1024)
        print(f"✅ ({size_mb:.1f}MB)")
        
        # Step 2: Post to FB
        print("   📤 Uploading to FB...", end=" ", flush=True)
        cap = caption_for(m)
        ok = post_to_fb(video_path, cap)
        
        # Step 3: Delete video
        try: os.remove(video_path)
        except: pass
        print(f"   🗑 Deleted local file")
        
        if ok:
            posted.add(key)
            save_posted(posted)
            count += 1
            print(f"   ✅ Done ({count}/{limit})")
        else:
            print(f"   ❌ FB upload failed, will retry next time")
        
        if count >= limit:
            break
        
        # Cooldown between posts (avoid FB rate limit)
        if count < limit:
            print("   ⏳ Waiting 30s...")
            time.sleep(30)
    
    # Cleanup old temp files
    clean_temp()
    print(f"\n✅ Posted {count} video(s) to FB page")

if __name__ == "__main__":
    main()
