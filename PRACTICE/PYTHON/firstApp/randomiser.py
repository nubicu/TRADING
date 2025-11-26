# -*- coding: utf-8 -*-
import random
import datetime

now = datetime.datetime.now()

print("Current date and time using strftime:")
print(now.strftime("%Y-%m-%d %H:%M:%S"))
print()


students = ["Alyssa", "Bridget", "Caroline", "Daisy", "Eleanor"]

print(random.choice(students))

print(random.randrange(4, 100))
print(random.randrange(-39, -9))