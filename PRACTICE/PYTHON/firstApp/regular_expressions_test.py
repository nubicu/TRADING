#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path

pattern = '^.*?\((\d+)\).*?$'
# ^     signifies the start of the string
#.*?    signifies anything after that
# \(    signifies the opening parenthesis
# (\d+) signifies one or more digits
# \)    signifies closing parenthesis
#.*?    signifies anything after the closing parenthesis
# $     signifies the end

test_string = 'Consumer number is (999)'
result = re.match(pattern, test_string)
if result:
    print('Consumer number is ' + str(result.group(1)))  # it has also groups()
else:
    print('No match')

data_file = Path(__file__).parent / 'sample.txt'
with data_file.open('r', encoding='utf-8') as f:
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', f.read())
print("Found " + str(len(emails)) + " emails in file")
for email in emails:
    print(email)

text = "software"
print(text[1:3])  # prints values in interval [1,3)

oldstring = 'i like Mihaela'
newstring = oldstring.replace('like', 'love')
print(newstring.capitalize())
print(':'.join(reversed(newstring.split(' '))))  # adds character ":" between words

a = {'x': 100, 'y': 200}
b = list(a.items())
print(b)

x = ("Rorico", 20, "Consulting")    # tuple packing
(company, emp, profile) = x    # tuple unpacking
print("Company " + company + " " + profile + " has " + str(emp) + " employees")


xx = """guru99
career guru 99
selenium"""
k1 = re.findall(r"^\w", xx)
k2 = re.findall(r"^\w", xx, re.MULTILINE)
print(k1)
print(k2)

list = ["guru99 get", "guru99 give", "guru Selenium"]
for element in list:
    z = re.match("(g\w+)\W(g\w+)", element)
if z:
    print((z.groups()))

patterns = ['software testing', 'guru99']
text = 'software testing is fun?'
for pattern in patterns:
    print('Looking for %s in %s ->' % (pattern, text), end=' ')
    if re.search(pattern, text):
        print('found a match!')
    else:
        print('no match')