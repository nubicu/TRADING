print("Hello, what's your name?")
name = input("My name is: ")
print("Hello, " + name + "!")
by = input("What's your birth year? ")
CURRENT_YEAR = 2025
age = CURRENT_YEAR - int(by)
print(name + ", you are " + str(age) + " years old in " + str(CURRENT_YEAR) + ".")