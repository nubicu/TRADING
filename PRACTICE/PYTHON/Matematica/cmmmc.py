# -*- coding: utf-8 -*-


def lcm(*args):
    """Calculates lcm (cmmmc) of args"""
    #find the largest of numbers:
    biggest = max(args)
    #the list of the numbers without the largest:
    rest = [n for n in args if n != biggest]
#the factor is to multiply with the biggest as long as the result of them is not divisble by all of the numbers in the rest
    factor = 1
    while True:
        #check if biggest is divisble by all in the rest:
        ans = False in [(biggest * factor) % n == 0 for n in rest]
        #if so the clm is found: break the loop and return it, otherwise increment the factor by 1 and try again:
        if not ans:
            break
        factor += 1
    biggest *= factor
    return "least common multiple of {0} is {1}".format(args, biggest)

if __name__ == "__main__":
    print(lcm(2, 3, 7))

    print("Execution terminated!")