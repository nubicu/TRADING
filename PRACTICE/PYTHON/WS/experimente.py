import math

counter = 0

def params1(x, y = 10):
    try:
        result = x + y
    except Exception:
        result = "Eroare"
    return result

def params2(*args):
    print(f"au fost pasate {len(args)} argumente")
    for i in range(len(args)):
        print(args[i], end=" ", flush=True)

def params3(**kwargs):
    print(f"au fost pasate {len(kwargs)} argumente")
    for i, (k, v) in enumerate(kwargs.items()):
        print(k,v)

def radical():
    pass

def main():
    print("Structura unui program in Python")
    structura_program()
    structura_program()
    structura_program()
    print(f"programul a fost apelat de {counter} ori")
    
    params2(1, 2, 3, 4, 5)
    print()
    params3(a=1, b=2, c=3)