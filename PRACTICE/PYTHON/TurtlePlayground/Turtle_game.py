#!/usr/bin/env python
# -*- coding: utf-8 -*-
import turtle
import time


def drawCircles(t, size):
    for i in range(10):
        t.circle(size)
        size = size - 4


def drawSpecial(t, size, repeat):
    for i in range(repeat):
        drawCircles(t, size)
        t.right(360 / repeat)

wn = turtle.Screen()
wn.bgcolor('black')

tina = turtle.Turtle()
tina.shape('turtle')

colors = ["red", "orange", "yellow", "green", "blue", "purple", "white"]
tina.goto(-160, 150)

for each_color in colors:
    tina.pendown()
    angle = 360 / len(colors)
    tina.color(each_color)
    tina.circle(40)
    tina.right(angle)
    tina.penup()
    tina.forward(30)

tina.goto(0, 0)

time.sleep(2)

tina.penup()
tina.begin_fill()
tina.color('green')
tina.goto(30, -150)
tina.pendown()
tina.circle(130)
tina.penup()
tina.end_fill()
tina.color('white')
tina.goto(0, 0)
tina.begin_fill()
tina.pendown()
tina.circle(20)
tina.penup()
tina.end_fill()
tina.begin_fill()
tina.color('black')
tina.pendown()
tina.circle(10)
tina.penup()
tina.end_fill()
tina.forward(60)
tina.right(45)
tina.begin_fill()
tina.color('white')
tina.pendown()
tina.circle(30)
tina.penup()
tina.end_fill()
tina.begin_fill()
tina.color('black')
tina.pendown()
tina.circle(10)
tina.penup()
tina.end_fill()
tina.right(90)
tina.forward(90)
tina.begin_fill()
tina.color('maroon')
tina.pendown()
tina.circle(40)
tina.penup()
tina.end_fill()
tina.goto(25, -25)
tina.write("Don't close this window!")

time.sleep(5)

Albert = turtle.Turtle()
Albert.speed(0)
Albert.color('white')
rotate = int(360)
drawSpecial(Albert, 150, 15)

St = turtle.Turtle()
St.speed(0)
St.color('orange')
rotate = int(90)
drawSpecial(St, 140, 14)

Steve = turtle.Turtle()
Steve.speed(0)
Steve.color('purple')
rotate = int(90)
drawSpecial(Steve, 130, 13)

Will = turtle.Turtle()
Will.speed(0)
Will.color('pink')
rotate = int(90)
drawSpecial(Will, 120, 12)

Wi = turtle.Turtle()
Wi.speed(0)
Wi.color('lightblue')
rotate = int(90)
drawSpecial(Wi, 100, 10)

time.sleep(5)