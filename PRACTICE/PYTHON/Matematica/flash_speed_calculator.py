def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Eroare: Impartire la zero!"
    return a / b

a = int(input("Introduceti un numar in baza 10: "))
b = int(input("Introduceti un numar in baza 10: "))

print(f"Suma: {add(a, b)}")
print(f"Diferenta: {subtract(a, b)}")
print(f"Produs: {multiply(a, b)}")
print(f"Cat: {divide(a, b)}")