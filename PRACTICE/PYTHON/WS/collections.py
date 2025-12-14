# Python collections module practice file
# from collections import Counter, defaultdict, namedtuple, deque

# integer index
list_properties : list  = ["ordered", "changeable", "collection", "duplicates"]
tuple_properties: tuple = ("ordered", "unchangeable", "collection", "duplicates")
# no index
set_properties  : set   = {"unordered", "unchangeable", "unindexed", "no_duplicates"}
# immutable index = key
dict_properties : dict  = {"ordered": True, "changeable": True, "duplicates": False}

# List
lista = list((list_properties, tuple_properties, set_properties, dict_properties))
# list[0] -> list[-1]
for array in lista:
    for item in array:
        print(item)

while len(lista) > 0:
    removed = lista.pop()
    print("Removed collection: ", removed)

nums = [1,2,3]
vals = nums
del vals[1:2]
print(nums)
print(vals)

print("Hello, what's your name?")
name = input("My name is: ")
print("Hello, " + name + "!")
by = input("What's your birth year? ")
CURRENT_YEAR = 2025
age = CURRENT_YEAR - int(by)
print(name + ", you are " + str(age) + " years old in " + str(CURRENT_YEAR) + ".")
