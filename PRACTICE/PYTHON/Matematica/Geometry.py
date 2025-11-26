#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Importing modules
import math


def circle_sphere_calc(r):
    #Calculations based of the radius
    d = r * 2
    #_circle is the calculation, where pi is also calculated
    PCirclePi = math.pi * r * 2
    SCirclePi = math.pi * r ** 2
    #_npi is the calculation, where pi (as a symbol) is left in
    PCircleNPi = r * 2
    SCircleNPi = r ** 2
    #Sphere area
    SSpherePi = 4 * math.pi * (r ** 2)
    SSphereNPi = 4 * (r ** 2)
    #Sphere volume
    VSpherePi = 4 / 3 * math.pi * (r ** 3)
    VSphereNPi = (r ** 3)

    #Output
    print()
    #Diameter
    print("Diameter(2*R) =", d)
    #Circle perimeter
    print("Perimeter(2*pi*R)=", "pi*{}".format(PCircleNPi), "or", PCirclePi)
    #Circle area
    print("Circle area(pi*R^2)=", "pi*{}".format(SCircleNPi), "or", SCirclePi)
    #Sphere area
    print("Sphere area =", "4*pi*{}". format(SSphereNPi) + "*{}".format(SCircleNPi), "or", SSpherePi)
    #Sphere volume
    print("Sphere volume(4/3*pi*R^3)=", "4/3*pi*{}".format(VSphereNPi), "or", VSpherePi)

print("Circle/Sphere calculator")
print("Note: Pi is equal to", math.pi)

#Getting the radius as input
r = int(input("Radius: "))
circle_sphere_calc(r)