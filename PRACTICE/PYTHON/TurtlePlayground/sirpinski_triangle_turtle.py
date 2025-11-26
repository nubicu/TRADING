from turtle import *
import turtle

t = turtle.Turtle()
t.ht()  # or turtle.hideturtle()
Window = turtle.Screen()

# Window.bgcolor('white')
Window.bgpic("background.gif")

penup()
goto(-200, -200)
# maximum speed for a turtle is 10 and 0 is fastest


def serp_tri(side, level):
    if level == 1:
        for i in range(3):
            turtle.color('black')
            turtle.ht()
            turtle.fd(side)
            turtle.left(120)
            turtle.speed(10)
    else:
        turtle.ht()
        serp_tri(side / 2, level - 1)
        turtle.fd(side / 2)
        serp_tri(side / 2, level - 1)
        turtle.bk(side / 2)
        turtle.left(60)
        turtle.fd(side / 2)
        turtle.right(60)
        serp_tri(side / 2, level - 1)
        turtle.left(60)
        turtle.bk(side / 2)
        turtle.right(60)
        turtle.speed(10)


def main():
    pendown()
    serp_tri(400, 8)

if __name__ == '__main__':
    main()
    turtle.mainloop()
    turtle.done()