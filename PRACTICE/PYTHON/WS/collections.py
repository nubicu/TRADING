# Python collections module practice file

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

'''
Pentru o lista de numere, scrieti o functie care gaseste si returneaza
valoarea maxima si numarul de aparitii a acesteia.
'''
in_list = [1.0, 2.33, 3, 4, 5, 1, 3, 5, 2, 4, 5, 1]
def max_and_count(numbers: list[float]) -> tuple[float, int]:
    if not numbers:
        return None, 0
    max_value = max(numbers)
    count = numbers.count(max_value)
    return max_value, count

max_val, occurrences = max_and_count(in_list)

'''
Scrie o functie care verifica daca un text este ordonat la nivelul fiecarui caracter.
'''
def is_ordered(text: str) -> bool:
    propozitie = text.replace(" ", "")
    clone = "".join(sorted(propozitie))
    return propozitie == clone

print(f"Max value: {max_val}, Occurrences: {occurrences}")
test_text = "abc de"
print(f"Is the text '{test_text}' ordered? {is_ordered(test_text)}")
test_text2 = "edc ba"
print(f"Is the text '{test_text2}' ordered? {is_ordered(test_text2)}")