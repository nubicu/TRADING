'''
Scrieti o functie care primeste ca parametru o propozitie
si afiseaza pe cate o linie, reprezentarea hex pentru codurile
ASCII a caracterelor din fiecare cuvant.
Practic orice cuvant va fi rescris pe o linie noua, dar in format hex
(cate 2 digiti per caracter, toti digitii uniti intre ei fara spatii).
Exemplu:pentru "abc 012" se va afisa:
616263
303132
'''
def formateaza(propozitie):
    cuvinte = propozitie.split()
    for cuvant in cuvinte:
        hex_cuvant = ''.join(format(ord(c),'02x') for c in cuvant)
        print(hex_cuvant)

'''
Scrieti o functie care primeste ca parametru urmatoarea propozitie:
"A fost, de asemenea, Remarcabil pentru Razboaiele persane si Pentru razboaiele Dintre orasele-state Grecesti."
Functia va returna numarul de caractere scrise cu majuscula.
'''
def numara(propozitie):
    count = 0
    for char in propozitie:
        if char.isupper():
            count += 1
    return count

# Exemplu de utilizare
formateaza("abc 012")
# Output:
# 616263
# 303132
formateaza("Hello World!")
# Output:
# 48656c6c6f
# 576f726c6421
propozitie = "A fost, de asemenea, Remarcabil pentru Razboaiele persane si Pentru razboaiele Dintre orasele-state Grecesti."
print(f"Numar caractere majuscule: {numara(propozitie)}")