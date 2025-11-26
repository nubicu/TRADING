# -*- coding: utf-8 -*-


class myClass():
    def method1(self):
        print("Guru99")


class childClass(myClass):
    def method1(self):
        myClass.method1(self)
        print("childClass Method1")

    def method2(self):
        print("childClass method2")


class User:
    name = ""

    def __init__(self, name):
        self.name = name

    def sayHello(self):
        print("Welcome to Guru99, " + self.name)


def main():
    # exercise the class methods
    c = myClass()
    c.method1()
    c2 = childClass()
    c2.method1()
    User1 = User("Alex")
    User1.sayHello()

if __name__ == "__main__":
    main()