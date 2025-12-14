'''
Scrieti o functie care primeste ca parametru o expresie matematica
cu paranteze rotunde si verifica daca parantezele sunt corect
inchise. Functia va returna True daca parantezele sunt corect
inchise si False in caz contrar.
'''

def expresie_corecta(expresie: str) -> bool:
    stiva = []
    for char in expresie:
        if char == '(':
            stiva.append(char)
        elif char == ')':
            if not stiva:
                return False
            stiva.pop()
    return len(stiva) == 0

# Teste
exp1 = "(a + b) * (c + d)"  # corecta
exp2 = "(a + b * (c - d)"   # incorecta
exp3 = "((a + b) * c) + d)"  # incorecta
print(expresie_corecta(exp1),True)  # ar trebui sa returneze True
print(expresie_corecta(exp2))  # ar trebui sa returneze False
print(expresie_corecta(exp3))  # ar trebui sa returneze False
print(expresie_corecta("a + b * c - d"),True)  # ar trebui sa returneze True
print(expresie_corecta("((a + b) * (c - d))"))  # ar trebui sa returneze True
print(expresie_corecta(")("))  # ar trebui sa returneze False
print(expresie_corecta("((())())"))  # ar trebui sa returneze True
print(expresie_corecta("((())(()"))  # ar trebui sa returneze False
print(expresie_corecta(")("))  # ar trebui sa returneze False
print(expresie_corecta("()()()"))  # ar trebui sa returneze True
print(expresie_corecta("((())())()"))  # ar trebui sa returneze True
print(expresie_corecta("((())())(()"))  # ar trebui sa returneze False
print(expresie_corecta(""))  # ar trebui sa returneze True
print(expresie_corecta("a + (b * c) - d"))  # ar trebui sa returneze True
print(expresie_corecta("a + b * c) - d("))  # ar trebui sa returneze False