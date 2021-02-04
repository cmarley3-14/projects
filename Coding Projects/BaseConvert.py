from math import *

def convertBase():
    chars = list(range(10)) + [chr(i) for i in range(ord("A"),ord("Z")+1)]
    number = int(input("Enter a number in base 10: "))
    base = int(input("Enter the base for conversion: "))
    power = floor(log(number, base))
    for i in range (power, -1, -1):
        print(chars[number // (base**i)], end='')
        number %= (base**i)
    print()

def convertBase_2(number, base):
    chars = list(range(10)) + [chr(i) for i in range(ord("A"),ord("Z")+1)]
    power = floor(log(number, base))
    for i in range (power, -1, -1):
        print(chars[number // (base**i)], end='')
        number %= (base**i)
    print()

while True:
    convertBase()
convertBase_2(984, 17)
convertBase_2(84564, 35)
convertBase_2(4564, 3)

        
