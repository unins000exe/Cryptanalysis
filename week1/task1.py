from random import shuffle
import math
from itertools import permutations
import json


def writef(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f'В {filename} было записано {data}')


def readf(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def gen_key(k):
    key = [i for i in range(k)]
    shuffle(key)
    writef("key1.txt", {'k': key})
    return key


def kasiski(s, min_num=3):
    out = ''

    matches = []
    found = {}
    for k in range(min_num, len(s) // 2):
        found[k] = {}
        shouldbreak = True
        for i in range(0, len(s) - k):
            v = s[i:i + k]
            if v not in found[k]:
                found[k][v] = 1
            else:
                found[k][v] += 1
                shouldbreak = False

        if shouldbreak:
            break

        for v in found[k]:
            if found[k][v] > 2:
                matches.append(v)

    out += "Длина  Количество  Слово   НОД  Положение (расстояние)\n"
    out += "=====  ==========  =====   ===  ======================\n"
    keylens = {}
    for v in matches:
        k = len(v)
        p = []
        for i in range(len(s)):
            if s[i:i + k] == v:
                p.append(i)

        factor = p[1] - p[0]
        for i in range(2, len(p)):
            factor = math.gcd(factor, p[i] - p[i - 1])

        if factor == 1:
            continue

        locations = ""
        for i in range(len(p)):
            locations += "%d " % p[i]
            if i > 0:
                locations += "(%d) " % (p[i] - p[i - 1])

        out += "%6d  %5d  %10s  %6d  %s\n" % (k, found[k][v], v, factor, locations)

    return out


def encrypt():
    key = readf("key1.txt")['k']
    k = len(key)
    key = key + [key[0]]

    with open("open_text.txt", "r", encoding='utf-8') as f:
        plaintext = f.read()

    f = open("enc_text.txt", 'w+')
    for i in range(len(plaintext) // k + 1):
        block = plaintext[i * k:(i + 1) * k]
        enc_block = [""] * k
        for j in range(len(block)):
            enc_block[key[j + 1]] = block[key[j]]
        f.write(''.join(enc_block))

    f.close()


def decrypt(k):
    with open("enc_text.txt", "r") as f:
        plaintext = f.read()

    f = open("dec_text.txt", 'w+')
    base = [i for i in range(k)]
    keys = list(permutations(base))
    for key in keys:
        key = list(key) + [key[0]]
        f.write('\nКлюч ' + str(key) + ":\n    ")
        for i in range(len(plaintext) // k + 1):
            enc_block = plaintext[i * k:(i + 1) * k]
            block = [""] * k
            for j in range(len(enc_block)):
                block[key[j + 1]] = enc_block[key[j]]
            f.write(''.join(block))

    f.close()


if __name__ == '__main__':
    while True:
        print("1 - Сгенерировать ключ")
        print("2 - Зашифровать текст")
        print("3 - Запустить тест Казиски")
        print("4 - Подобрать ключ")
        option = int(input("Выберите опцию: "))
        if option == 1:
            k = int(input("Введите длину ключа"))
            key = gen_key(k)
            print('Ключ', key)
        elif option == 2:
            encrypt()
            print("Текст из файла open_text.txt зашифрован, результат записан в enc_text.txt\n")
        elif option == 3:
            with open("enc_text.txt", 'r') as et:
                s = et.read()
                out = kasiski(s)
            with open("kasiski.txt", "w") as kf:
                kf.write(out)
            print("Результат теста Казиски записан в файл kasiski.txt\n")
        elif option == 4:
            k = int(input("Введите длину ключа "))
            decrypt(k)
            print("Текст из файла enc_text.txt расшифрован, результат записан в dec_text.txt\n")
        else:
            break
