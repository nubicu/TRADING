# -*- coding: utf-8 -*-
import os
import urllib
import urllib.parse
import urllib.request
import urllib.error
import json

BASE_URL = "https://serpapi.com/search.json"

query_text = input("What do you want to search for ? >> ")
print("Please wait while search takes place!")

# Get API key from environment first, then prompt the user if not set
api_key = os.getenv('SERPAPI_KEY') or os.getenv('SERPAPI_API_KEY')
if not api_key:
    api_key = input("Enter your SerpApi API key (set SERPAPI_KEY to avoid this prompt): ").strip()
    if not api_key:
        print("No API key provided. Visit https://serpapi.com to get an API key.")
        raise SystemExit(1)

# Build parameters explicitly (include locale params)
params = {
    'q': query_text,
    'api_key': api_key,
    'hl': 'en',
    'gl': 'us',
    'engine': 'google'
}

full_url = BASE_URL + "?" + urllib.parse.urlencode(params)

try:
    with urllib.request.urlopen(full_url, timeout=15) as resp:
        raw = resp.read()
except urllib.error.HTTPError as e:
    if e.code == 401:
        print("HTTP 401 Unauthorized: your SerpApi API key is missing or invalid.")
        print("Set the environment variable `SERPAPI_KEY` or provide a valid key.")
        try:
            detail = e.read().decode('utf-8', errors='ignore')
            if detail:
                print("Server response:", detail)
        except Exception:
            pass
        raise
except urllib.error.URLError as e:
    print("Failed to reach SerpApi:", e)
    raise

try:
    data = json.loads(raw)
except Exception as e:
    print("Failed to parse JSON response:", e)
    raise

print()
print("Displaying search results :")
results = data.get("organic_results") or data.get('organic') or []
if not results:
    print("No organic results returned. Full response keys:", list(data.keys()))
else:
    for item in results:
        title = item.get('title') or item.get('name') or '<no title>'
        link = item.get('link') or item.get('link') or '<no link>'
        print(f"{title} - Link: {link}")