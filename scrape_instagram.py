import requests
import json
import os
from datetime import datetime

# Load your API key from GitHub Secrets
API_KEY = os.getenv("SCRAPEDO_API_KEY")

# Scrape.do endpoint for Instagram comments
BASE_URL = "https://api.scrape.do/v1/scrape"

# Target Instagram account
username = "worldhorseracing"

# Define the date range for May 2025
start_date = datetime(2025, 5, 1)
end_date = datetime(2025, 5, 31)

# Step 1: Get posts from the account
params = {
    "api_key": API_KEY,
    "url": f"https://www.instagram.com/{username}/",
    "render": "true"
}

print("Fetching posts...")
response = requests.get(BASE_URL, params=params)
data = response.json()

# Extract post URLs (you may need to adjust this depending on Scrape.do's response structure)
post_urls = []
for item in data.get("posts", []):
    post_date = datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%S")
    if start_date <= post_date <= end_date:
        post_urls.append(item["url"])

print(f"Found {len(post_urls)} posts from May 2025.")

# Step 2: Scrape comments from each post
all_comments = []

for url in post_urls:
    print(f"Scraping comments from: {url}")
    comment_params = {
        "api_key": API_KEY,
        "url": url,
        "render": "true"
    }
    comment_response = requests.get(BASE_URL, params=comment_params)
    comment_data = comment_response.json()

    comments = comment_data.get("comments", [])
    for comment in comments:
        all_comments.append({
            "post_url": url,
            "username": comment.get("username"),
            "text": comment.get("text"),
            "timestamp": comment.get("timestamp")
        })

# Step 3: Save to file
with open("comments.json", "w", encoding="utf-8") as f:
    json.dump(all_comments, f, indent=2, ensure_ascii=False)

print(f"Saved {len(all_comments)} comments to comments.json")
      - name: Upload comments.json as artifact
        uses: actions/upload-artifact@v3
        with:
          name: comments-json
          path: comments.json

