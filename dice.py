from random import randint

def dice(num, sides):
    return sum([randint(1, sides) for i in range(num)])
