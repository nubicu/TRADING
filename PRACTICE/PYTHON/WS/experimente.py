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

def structura_program():
    global counter
    x = 10
    if x < 8:
        print(f"{x} < 8 : {x<8}")
    else:
        print(f"{x} >= 8 : {x>=8}")

    ok = False
    cnt = 0
    if x > 5:
        ok = False
        cnt = 1
    elif x > 9:
        ok = True
        cnt = 2
    elif x < 8:
        ok = False
        cnt = 3
    else:
        ok = True
        cnt = 4

    if not ok:
        print(f"ok = {ok}")

    print(f"cnt = {cnt}")

    for i in range(10):
        print(i)
    
    i = 0
    while i < 10:
        print(i, end=" ", flush=True)
        i += 1
    print(" ")

    counter += 1

# Aici calculam radical si separam partea intreaga de cea zecimala
def radical(nr) -> tuple[int, int]:
    r = math.sqrt(nr)
    ip = int(r)
    rp = int(round(r,2) * 100) % 100
    return ip, rp

def ID():
    s_nr = input("Introduceti numarul: ")
    print(f"Numarul introdus este {s_nr}")
    print("Tipul de date este ", type(s_nr))
    n_nr = int(s_nr)
    print(f"Tipul de date convertit este ", type(n_nr))

def strings1():
    data = "   Daca invat la Python primesc note intre 2 si 10"
    _10 = data[-2:]
    print(_10)
    _2 = data[-7:-6]
    print(_2)
    lung = len(data)
    print(f"Lungimea sirului este {lung}")
    nn = int(_10) + int(_2)
    print(f"Suma numerelor extrase este {nn}")
    c1 = ord(data[4])
    c2 = ord(data[-1])
    print(f"Codul ASCII al caracterului {data[4]} este {c1}, iar al ultimului caracter este {c2}")
    binar_n = bin(nn)
    hexa_n = hex(nn)
    print(f"Numarul {nn} in binar este {binar_n}, iar in hexazecimal este {hexa_n}")
    count_a = data.lower().count("a")
    print(count_a)
    data_l = data.lower()
    data_u = data.upper()
    print(data_l)
    print(data_u)
    words = data.split()
    print(words)
    stripped = data.strip()
    print(stripped)
    new_data = data.replace("Python", "orice materie")
    print(new_data)

    if data.strip().lower().startswith("daca"):
        print("Propozitia incepe cu \"Daca\"")
    for i in range(1, 100):
        if data.strip().lower().endswith(str(i)):
            print(f"Propozitia se termina cu valoarea numerica {i}")
            break

def strings2():
    x = "ana are mere"
    y = "mihai merge la munte"
    z = " ".join([x.split()[0], " ".join(y.split()[1:]), "si", y.split()[0], " ".join(x.split()[1:])])
    print(z)

def numere() -> float:
    a = 100
    x = str(a)
    r = round(math.sqrt(a), 5)
    r1 = math.ceil(r)
    r2 = math.floor(r)
    print(a, x, r, r1, r2)
    return r+a+r1+r2

def main():
    print("Structura unui program in Python")
    structura_program()
    structura_program()
    structura_program()
    print(f"programul a fost apelat de {counter} ori")
    
    print("Radical -------------")
    print(" ")
    i, r = radical(2)
    print(i, r)
    i, _ = radical(49)
    print(i)

    print("Input/Output -------------")
    print(" ")
    ID()

    print("Parametri -------------")
    print(" ")
    r0 = params1(4.5, 15)
    print(r0)
    r1 = params1(15, 20)
    print(r1)
    r2 = params1("Hello", " Python")
    print(r2)
    r3 = params1("abc ")
    print(r3)

    print(" ")
    params2(4, 9, "xyz")
    params3(size = 21, elem = "a", p1 = 4, p2 = "AAA")

    print("Numere -------------")
    numere()

    print("Siruri de caractere -------------")
    strings1()
    strings2()


if __name__ == "__main__":
    main()