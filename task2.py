from random import shuffle, randint
import math
import re

ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
numbers = '1234567890'
symbols = [*ru, *en, *punc, *numbers]


def normalize(s, flag):
    s = s.strip().upper()
    if flag:
        s = re.sub(r'[^А-Я]+', '', s)
    else:
        s = re.sub(r'[^A-Z]+', '', s)
    return s


def random_text(lenght, number):
    for n in range(number):
        out = ''
        for i in range(lenght):
            out += symbols[randint(0, len(symbols) - 1)]
        with open("random" + str(n) + ".txt", 'w') as rf:
            rf.write(out)


def index(y, z):
    n = len(y)
    if len(z) < len(y):
        n = len(z)

    ind = 0
    for i in range(n):
        if y[i] == z[i]:
            ind += 1

    return ind / n * 100


def call_ind(filename1, filename2, outname):
    if filename1[0:6] == 'random':
        with open(filename1, 'r', encoding='windows-1251') as f:
            y = f.read()
        with open(filename2, 'r', encoding='windows-1251') as f:
            z = f.read()
    else:
        with open(filename1, 'r', encoding='utf-8') as f:
            y = f.read()
        with open(filename2, 'r', encoding='utf-8') as f:
            z = f.read()

    if filename1[0:2] == 'en':
        y = normalize(y, False)
        z = normalize(z, False)
    elif filename1[0:2] == 'ru':
        y = normalize(y, True)
        z = normalize(z, True)

    res = open(outname, 'w+')

    res.write(filename1 + ' < > ' + filename2 + " " + str(index(y, z)) + '\n')

    res.close()


def call_ind_task3(filename1, outname):
    if filename1[0:6] == 'random':
        with open(filename1, 'r', encoding='windows-1251') as f:
            y = f.read()
    else:
        with open(filename1, 'r', encoding='utf-8') as f:
            y = f.read()

    if filename1[0:2] == 'en':
        y = normalize(y, False)
    elif filename1[0:2] == 'ru':
        y = normalize(y, True)

    res = open(outname, 'w+')
    y2 = y[-1:] + y[:-1]
    for l in range(0, 15):
        res.write(filename1 + " " + str(index(y, y2)) + '\n')
        y2 = y2[-1:] + y2[:-1]

    res.close()


def ind_avg(filename1, filename2):
    if filename1[0:6] == 'random':
        with open(filename1, 'r', encoding='windows-1251') as f:
            y = f.read()
        with open(filename2, 'r', encoding='windows-1251') as f:
            z = f.read()
    else:
        with open(filename1, 'r', encoding='utf-8') as f:
            y = f.read()
        with open(filename2, 'r', encoding='utf-8') as f:
            z = f.read()

    n = len(y)
    if len(z) < len(y):
        n = len(z)

    y = y[0:n]
    z = z[0:n]

    if filename1[0:2] == 'en':
        y = normalize(y, False)
        z = normalize(z, False)
        freq1 = dict(zip(en, [y.count(i) for i in en]))
        freq2 = dict(zip(en, [z.count(i) for i in en]))
    elif filename1[0:2] == 'ru':
        y = normalize(y, True)
        z = normalize(z, True)
        freq1 = dict(zip(ru, [y.count(i) for i in ru]))
        freq2 = dict(zip(ru, [z.count(i) for i in ru]))
    else:
        freq1 = dict(zip(symbols, [y.count(i) for i in symbols]))
        freq2 = dict(zip(symbols, [z.count(i) for i in symbols]))

    n = len(y)
    if len(z) < len(y):
        n = len(z)

    ind_avg = 0
    for key in freq1.keys():
        ind_avg += freq1[key] * freq2[key] / (n * n)

    return ind_avg * 100


def call_ind_avg(folder, number=20):
    res = open('res_avg_' + folder + '.txt', 'w+')

    for i in range(number // 2):
        file1 = folder + '/' + folder + str(i) + '.txt'
        file2 = folder + '/' + folder + str(number - 1 - i) + '.txt'
        res.write(file1 + ' < > ' + file2 + " " + str(ind_avg(file1, file2)) + '\n')

    res.close()



def vigenere_cipher(text, alphabet, key, mode):
    result = ''
    key_index = 0

    for char in text:
        if char in alphabet:
            if mode == 'encrypt':
                char_index = (alphabet.index(char) + alphabet.index(key[key_index])) % len(alphabet)
            elif mode == 'decrypt':
                char_index = (alphabet.index(char) - alphabet.index(key[key_index])) % len(alphabet)
            result += alphabet[char_index]
            key_index = (key_index + 1) % len(key)
        else:
            result += char

    return result


def call_vigenere_enc():
    text_file = input('Введите имя файла для зашифрования (без .txt) ')

    with open('key.txt', 'r', encoding='utf-8') as k:
        key = k.read()

    if text_file[0:2] == 'ru':
        with open(text_file + '.txt', 'r', encoding='utf-8') as t:
            text = normalize(t.read(), True)
        with open(text_file + '_enc.txt', 'w', encoding='utf-8') as te:
            te.write(vigenere_cipher(text, ru, key, 'encrypt'))
    elif text_file[0:2] == 'en':
        with open(text_file + '.txt', 'r', encoding='utf-8') as t:
            text = normalize(t.read(), False)
        with open(text_file + '_enc.txt', 'w', encoding='utf-8') as te:
            te.write(vigenere_cipher(text, en, key, 'encrypt'))
    else:
        with open(text_file + '.txt', 'r', encoding='utf-8') as t:
            text = t.read()
        with open(text_file + '_enc.txt', 'w', encoding='utf-8') as te:
            te.write(vigenere_cipher(text, symbols, key, 'encrypt'))


def call_vigenere_dec():
    text_file = input('Введите имя файла для расшифрования (без _enc.txt) ')

    with open('key.txt', 'r', encoding='utf-8') as k:
        key = k.read()

    if text_file[0:2] == 'ru':
        with open(text_file + '_enc.txt', 'r', encoding='utf-8') as t:
            text = t.read()
        with open(text_file + '_dec.txt', 'w', encoding='utf-8') as te:
            te.write(vigenere_cipher(text, ru, key, 'decrypt'))
    elif text_file[0:2] == 'en':
        with open(text_file + '_enc.txt', 'r', encoding='utf-8') as t:
            text = t.read()
        with open(text_file + '_dec.txt', 'w', encoding='utf-8') as te:
            te.write(vigenere_cipher(text, en, key, 'decrypt'))
    else:
        with open(text_file + '_enc.txt', 'r', encoding='utf-8') as t:
            text = t.read()
        with open(text_file + '_dec.txt', 'w', encoding='utf-8') as te:
            te.write(vigenere_cipher(text, symbols, key, 'decrypt'))


if __name__ == '__main__':
    # call_ind_avg('ru')
    # call_ind_avg('en')
    # call_ind_avg('random')

    call_vigenere_enc()
    # call_vigenere_dec()
    call_ind_task3('ru/ru2_enc.txt', 'ru2_enc5_task3.txt')


