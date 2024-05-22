# -*- coding: utf-8 -*-
import json
from itertools import combinations_with_replacement
from math import prod


def sieve_of_erato(n):
    a = [i for i in range(n + 1)]

    a[1] = 0
    i = 2
    while i * i <= n:
        if a[i] != 0:
            j = i ** 2
            while j <= n:
                a[j] = 0
                j = j + i
        i += 1

    a = [i for i in a if i != 0]
    return a


def writef(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    # print(f'В {filename} было записано {data}')


def readf(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# primes = sieve_of_erato(1000)
# writef('prime_base.json', {'primes': primes})


while True:
    opt = int(input("1 - создание базы, 2 - метод пробного деления. Ваш выбор: "))
    if opt == 1:
        t = int(input('Введите число простых множителей t '))
        primes = readf('prime_base.json')['primes']
        mult_base = {}
        for mult in combinations_with_replacement(primes, t):
            mult_base[prod(mult)] = mult

        writef('mult_base.json', mult_base)
    elif opt == 2:
        mult_base = readf('mult_base.json')
        n = int(input('Введите число для разложения на множители '))
        if str(n) in list(mult_base.keys()):
            print(mult_base[str(n)])
        else:
            print('Не удалось разложить число')
    else:
        break




