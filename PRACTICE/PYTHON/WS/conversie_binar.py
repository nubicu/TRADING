'''
Scrieti o functie care converteste un numar din baza 10 in baza 2
Functia va primi ca arametru numarul in baza 10
si va returna un sir de caractere reprezentand numarul in baza 2
Numerele convertite in baza 2 vor avea la inceput prefixul '0b'
Exemplu: pentru numarul 10, functia va returna '0b101
'''
def conversie_binar(n: int) -> str:
    if n == 0:
        return "0"
    bits = []
    while n > 0:
        bits.append(str(n % 2))
        n //= 2
    bits.reverse()
    return ''.join(bits)

'''
Scrieti o functie care primste 2 parametri: un sir de 4 caractere si un numar intreg
Functia va converti numarul din baza 10, in baza data de lungimea
sirului de caractere
Exemplu: sir = "abcd" => baza 4
         nr = 301
         301 / 4 = 75 rest 1
         75 / 4 = 18 rest 3
         18 / 4 = 4 rest 2
         4 / 4 = 1 rest 0
         1 / 4 = 0 rest 1
         resturile in ordine inversa sunt 10231 dar vom folosi cifrele
         pe post de indecsi in sirul de caractere
'''
def conversie_ciudata(s: str, n: int) -> str:
    baza = len(s)
    if n == 0:
        return s[0]
    cifre = []
    while n > 0:
        cifre.append(s[n % baza])
        n //= baza
    cifre.reverse()
    return ''.join(cifre)


nr = int(input("Introduceti un numar in baza 10: "))
rez = conversie_binar(nr)
print(f"Numarul {nr} in baza 2 este: 0b{rez}")
print(bin(nr))  # Verificare cu functia bin incorporata

rez = conversie_ciudata("abcd", 301)  # ar trebui sa returneze "bacdb"
print(f"Rezultatul conversiei este: {rez}")