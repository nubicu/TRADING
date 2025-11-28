# -*- coding: utf-8 -*-

Dict = {'Tim': 18, 'Charlie': 12, 'Tiffany': 22, 'Robert': 25}
print("Initial dictionary: ", Dict)
print(Dict['Tiffany'])
Dict.update({'Sarah': 9})
del Dict['Charlie']
Dict.update({'Robert': 39})
print(Dict)
print("Length : %d" % len(Dict))

print("variable Type: %s" % type(Dict))

print("Students Name: %s" % list(Dict.items()))

Boys = {'Tim': 18, 'Charlie': 12, 'Robert': 25}
Girls = {'Tiffany': 22}
studentX = Boys.copy()
studentY = Girls.copy()
print(studentX)
print(studentY)

for key in list(Dict.keys()):
    if key in list(Boys.keys()):
        print(key + " " + str(True))
    else:
        print(key + " " + str(False))
print
Students = list(Dict.keys())
Students.sort()
for S in Students:
    print(":".join((S, str(Dict[S]))))

print("printable string:%s" % str(Dict))

x = 20
y = 20
if (x is y):
    print("x & y  SAME identity")
y = 30
if (x is not y):
    print("x & y have DIFFERENT identity")

v = 4
w = 5
x = 8
y = 2
z = (v + w) * x / y
print("Value of (v + w) * x / y is %d" % z)


def main():
    x, y = 10, 8
    st = "x is less than y" if (x < y) else "x is greater than or equal to y"
    print(st)
    for x in range(13, 16):
        #if (x == 15): break
        if (x % 5 == 0):
            continue
        print(x)


def SwitchExample(argument):
    switcher = {
        0: " This is Case Zero ",
        1: " This is Case One ",
        2: " This is Case Two ",
    }
    return switcher.get(argument, "nothing")


if __name__ == "__main__":
    argument = 0
    print(SwitchExample(argument))
    main()

for i in '123':
    print("guru99", i)