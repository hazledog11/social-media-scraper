import requests
import json
import os
from datetime import datetime

# Load your Scrape.do API key from GitHub Secrets
API_KEY = os.getenv("SCRAPEDO_API_KEY")
BASE_URL = "https://api.scrape.do/v1/scrape"
USERNAME = "worldhorseracing"

# Define the date range for May 2025
start_date = datetime(2025, 5, 1)
end_date = datetime(2025, 5, 31)

# Step 1: Fetch the Instagram profile page
print("Fetching Instagram profile...")
profile_url = f"https:www.instagram.com/worldhorseracing/"
params = {
    "api_key": API_KEY,
    "url": profile_url,
    "render": "true"
}

try:
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    profile_data = response.json()
except Exception as e:
    print(f"Failed to fetch profile: {e}")
    profile_data = {}

# Save raw profile response for debugging
with open("profile_raw.json", "w", encoding="utf-8") as f:
    json.dump(profile_data, f, indent=2, ensure_ascii=False)

# Step 2: Extract post URLs
post_urls = []
posts = profile_data.get("posts") or profile_data.get("data") or []

print(f"Found {len(posts)} items in profile data.")

for post in posts:
    try:
        post_url = post.get("url") or post.get("shortcode_url") or post.get("link")
        timestamp = post.get("timestamp") or post.get("taken_at_timestamp")

        # Convert timestamp to datetime
        if isinstance(timestamp, (int, float)):
            post_date = datetime.fromtimestamp(timestamp)
        elif isinstance(timestamp, str):
            try:
                post_date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                post_date = None
        else:
            post_date = None

        if post_url and post_date and start_date <= post_date <= end_date:
            post_urls.append(post_url)
    except Exception as e:
        print(f"Error parsing post: {e}")

print(f"Filtered {len(post_urls)} posts from May 2025.")

# Step 3: Scrape comments from each post
all_comments = []

for index, url in enumerate(post_urls):
    print(f"Scraping comments from: {url}")
    comment_params = {
        "api_key": API_KEY,
        "url": url,
        "render": "true"
    }

    try:
        comment_response = requests.get(BASE_URL, params=comment_params)
        comment_response.raise_for_status()
        comment_data = comment_response.json()

        # Save raw comment data for each post
        with open(f"comments_raw_{index}.json", "w", encoding="utf-8") as f:
            json.dump(comment_data, f, indent=2, ensure_ascii=False)

        comments = comment_data.get("comments") or comment_data.get("data") or []
        for comment in comments:
            all_comments.append({
                "post_url": url,
                "username": comment.get("username"),
                "text": comment.get("text"),
                "timestamp": comment.get("timestamp")
            })

    except Exception as e:
        print(f"Failed to scrape comments from {url}: {e}")

# Step 4: Save all comments
with open("comments.json", "w", encoding="utf-8") as f:
    json.dump(all_comments, f, indent=2, ensure_ascii=False)

print(f"Saved {len(all_comments)} comments to comments.json")
