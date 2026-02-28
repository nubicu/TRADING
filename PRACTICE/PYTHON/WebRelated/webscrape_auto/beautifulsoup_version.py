import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

"""
Best practices for debugging your selectors:
# Print the raw HTML first to see what you're actually working with
print(response.text[:3000])

# Then test your selector on just one element
first_row = soup.find("tr", class_="athing")
print(first_row)
# Then find the title and link within that row
title_tag = first_row.find("span", class_="titleline")
print(title_tag)
link = title_tag.find("a")
print(link.text)
print(link["href"])
"""

articles = []

# Each story row has class "athing"
for row in soup.find_all("tr", class_="athing"):
    title_tag = row.find("span", class_="titleline")
    if not title_tag:
        continue

    link = title_tag.find("a")
    if not link:
        continue

    headline = link.text
    href = link["href"]

    # The score is in the NEXT <tr> after this one
    next_row = row.find_next_sibling("tr")
    if not next_row:
        continue

    score_tag = next_row.find("span", class_="score")
    points = int(score_tag.text.split()[0]) if score_tag else 0

    articles.append((headline, href, points))

# Sort by points descending
articles.sort(key=lambda x: x[2], reverse=True)

# Print top 10 articles with their points
for i, (headline, href, points) in enumerate(articles[:10]):
    print(f"{i+1}. {headline}")
    print(f"   URL: {href}")
    print(f"   Points: {points}")
    print()