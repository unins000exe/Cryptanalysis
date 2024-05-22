from random import randint
from math import gcd, log, floor, sqrt, ceil
from sympy import isprime, sieve, legendre_symbol
from itertools import combinations
from numpy import sum as npsum
import time


def pollards_rho(n, eps):
    if n & 1 == 0:
        return 2
    t = 4 * floor(sqrt(2 * sqrt(n) * log(1 / eps))) + 1

    def f(x):
        return (x * x + 1) % n

    xi, xk = randint(1, n - 1), 1
    i, k = 0, 2
    for _ in range(t):
        if gcd(n, abs(xi - xk)) == n:
            xi, xk = randint(1, n - 1), 1
            i, k = 0, 2
        if i == k:
            xk = xi
            k *= 2
        xi = f(xi)
        i += 1
        if gcd(n, abs(xi - xk)) != 1:
            return gcd(n, abs(xi - xk))

    return n


def p_rho_factorization(n, eps):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    factors = []
    for p in primes:
        if n % p == 0:
            n //= p
            factors.append(p)
    while n != 1:
        d = pollards_rho(n, eps)
        n //= d
        factors.append(d)
    return factors


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


def gcd_extended(num1, num2):
    if num1 == 0:
        return num2, 0, 1
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return div, y - (num2 // num1) * x, x


def congruence_relation(a, b, m):
    d, u, v = gcd_extended(a, m)
    if d > 1:
        if b % d != 0:
            print('Нет решений сравнения.')
            return None
        else:
            b //= d
            m //= d

    x = int(u * b % m)
    return x


def pollards_p1(n, t, big_b):
    for _ in range(floor(log(big_b)) + 10):
        a = randint(2, n - 2)
        d = gcd(a, n)
        if d == 1:
            b = congruence_relation(1, pow(a, t, n) - 1, n)
        else:
            return 1, d
        n1 = gcd(b, n)
        if n1 == n:
            continue
        if n1 > 1:
            return 1, n1
        if n1 == 1:
            return -1, None
    return 0, None


def call_pollards_p1(n):
    big_b = randint(floor(sqrt(n)) // 10 + 2, floor(sqrt(n)))
    qs, t = list(sieve.primerange(big_b)), 1

    for qi in qs:
        t *= pow(qi, int(log(n) // log(qi)))
    result, d = pollards_p1(n, t, big_b)

    if d is None:
        return pollards_rho(n, 0.01)

    while d is None:
        if result == 0:
            big_b //= 2
        if result == -1:
            big_b *= 2

        qs, t = list(sieve.primerange(big_b)), 1
        for qi in qs:
            t *= pow(qi, int(log(n) // log(qi)))
        result, d = pollards_p1(n, t, big_b)

    return d


def pp1_factorization(n):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    factors = []
    for p in primes:
        if n % p == 0:
            n //= p
            factors.append(p)

    while n != 1:
        d = call_pollards_p1(n)
        n //= d
        factors.append(d)
        if isprime(n):
            factors.append(n)
            return factors
    return factors


# 1557697, 21299881, 3865489, 32880121853, 15053151547, 991258173307575289
if __name__ == '__main__':
    n = int(input('Введите число '))

    time0 = time.time()
    print('Факторизация rho-методом Полларда', p_rho_factorization(n, 0.01))
    print(f'{time.time() - time0} секунд.\n')

    time0 = time.time()
    print('Факторизация (p-1)-методом Полларда', pp1_factorization(n))
    print(f'{time.time() - time0} секунд.\n')

    # time0 = time.time()
    # print('Факторизация алгоритмом Бриллхарта-Моррисона', p_rho_factorization(n, 0.01))
    # print(f'{(time.time() - time0) * 5} секунд.\n')


