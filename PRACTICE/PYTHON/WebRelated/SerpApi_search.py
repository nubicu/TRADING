# -*- coding: utf-8 -*-
import urllib
import urllib.parse
import urllib.request
import json

# API key : AIzaSyBHE99GfAx7V8d6uleSoVOVnDQgKjFXndw
url = "https://serpapi.com/search.json?hl=en&gl=us"

query = input("What do you want to search for ? >> ")

print("Please wait while search takes place!")

query = urllib.parse.urlencode({'q': query})

response = urllib.request.urlopen(url + "&" + query).read()

data = json.loads(response)

print()
print("Displaying search results :")
results = data["organic_results"]
for result in results:
    title = result['title']
    url = result['link']
    print(title + ' - Link: ' + url)