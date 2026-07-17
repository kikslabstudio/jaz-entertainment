import requests, json, re
from bs4 import BeautifulSoup

BASE_URL = "https://mlfbd.com"
IMDB_API_URL = "https://graph.imdbapi.dev/v1/movie/search?q="

def get_all_post_links():
    urls = [BASE_URL]
    categories = [
        "hollywood", "web-series", "dual-audio", "hindi-dubbed", "netflix", "action", "sci-fi"
    ]
    urls += [f"{BASE_URL}/category/{cat}/" for cat in categories]

    post_links = set()
    for url in urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.select("h2.entry-title > a"):
            post_links.add(a['href'])
    return list(post_links)

def scrape_movie_details(post_url):
    try:
        res = requests.get(post_url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        title_tag = soup.find("h1", class_="entry-title")
        title = title_tag.text.strip() if title_tag else "Unknown"

        video = soup.find("iframe")
        video_play = video['src'] if video else ""

        links = soup.find_all("a", href=True)
        download_link = ""
        for link in links:
            if any(x in link.text.lower() for x in ['download', '480p', '720p', '1080p']):
                download_link = link['href']
                break

        imdb_res = requests.get(IMDB_API_URL + title)
        imdb_data = imdb_res.json()
        movie_data = imdb_data['results'][0] if imdb_data.get("results") else {}

        return {
            "title": title,
            "poster": movie_data.get("image", ""),
            "rating": movie_data.get("rating", 0),
            "release_date": movie_data.get("year", ""),
            "genres": movie_data.get("genreList", []),
            "video_play": video_play,
            "download_link": download_link
        }

    except Exception as e:
        print(f"❌ Error: {post_url} -> {e}")
        return None

# Main logic
print("🔍 Scraping MLFBD + IMDb...")
posts = get_all_post_links()[:15]  # Limit to 15 for safety
movies = []

for post_url in posts:
    print(f"🎬 {post_url}")
    data = scrape_movie_details(post_url)
    if data:
        movies.append(data)

# Save to movies.json
with open("movies.json", "w", encoding="utf-8") as f:
    json.dump(movies, f, indent=2, ensure_ascii=False)

print("✅ movies.json updated successfully.")
