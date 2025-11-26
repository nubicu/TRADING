# -*- coding: utf-8 -*-
import whois

data = input("Enter a domain: ")
w = whois.whois(data)

print(w)