# -*- coding: utf-8 -*-
import urllib.request as u
import re

#connect to a URL
website = u.urlopen("https://www.geeksforgeeks.org/python-strings/")

#read html code
html = website.read().decode('utf-8')

#use re.findall to get all the links
links = re.findall('href="((http|ftp)s?://.*?)"', html)

print("Found %d links on the website:" % len(links))

for link in links:
    print(link[0])