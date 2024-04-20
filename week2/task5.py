# -*- coding: utf-8 -*-
import json
import re


def writef(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print(f'В {filename} было записано {data}')


def readf(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def get_alphabet():
    with open("open_text.txt", 'r', encoding='utf-8') as file:
        text = file.read()
        alphabet = ''.join(sorted(list(set(text))))

    writef("alphabet.txt", {'alphabet': alphabet})
    return alphabet


def frequency(file):
    alphabet = readf('alphabet.txt')['alphabet']
    freq = dict(zip(alphabet, [0] * len(alphabet)))
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        n = len(text)
        for c in text:
            if c in freq.keys():
                freq[c] += 1

    for c in freq:
        freq[c] /= n

    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    writef('freq_' + file, freq)


def frequency2(text):
    alphabet = readf('alphabet.txt')['alphabet']
    freq = dict(zip(alphabet, [0] * len(alphabet)))
    n = len(text)
    for c in text:
        if c in freq.keys():
            freq[c] += 1

    for c in freq:
        freq[c] /= n

    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    return freq


def vigenere_cipher(mode):
    result = ''
    key_index = 0
    alphabet = readf('alphabet.txt')['alphabet']

    with open('open_text.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    with open('key5.txt', 'r', encoding='utf-8') as f:
        key = f.read()

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

    with open('enc_text.txt', 'w', encoding='utf-8') as f:
        f.write(result)


def shift_lst(lst, sh):
    return lst[-sh:] + lst[:-sh]


def word_freq():
    with open('big_text2.txt', 'r', encoding='utf-8') as f:
        big_text = f.read().lower()
    freq = dict()
    match_pattern = re.findall(r'\b[а-я]{3,15}\b', big_text)
    for word in match_pattern:
        count = freq.get(word, 0)
        freq[word] = count + 1

    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    writef('words_freq.txt', freq)


def freq_attack(k):
    alphabet = readf('alphabet.txt')['alphabet']
    n = len(alphabet)
    with open('enc_text.txt', 'r', encoding='utf-8') as f:
        enc_text = f.read()

    freq_big_text = readf('freq_big_text.txt')

    most = list(freq_big_text.keys())[0]

    enc_k = [''] * k
    current_k = 0
    for c in enc_text:
        enc_k[current_k] += c
        current_k = (current_k + 1) % k

    keys = [[''] * k for _ in range(k)]

    for i in range(k):
        freq_enc = frequency2(enc_k[i])
        freq_elist = list(freq_enc.keys())

        for j in range(k):
            sh = (alphabet.index(freq_elist[j]) - alphabet.index(most)) % n
            keys[j][i] = alphabet[sh]
    writef('keys5.txt', {'keys': keys})


def word_attack(k, word):
    with open('enc_text.txt', 'r', encoding='utf-8') as f:
        enc_text = f.read()
    # words_freq = readf('words_freq.txt')
    alphabet = readf('alphabet.txt')['alphabet']
    n = len(alphabet)

    keys = []
    long_word = ''
    for i in range(k):
        long_word += word[i % len(word)]

    for t in range(len(enc_text) // k):
        y = enc_text[t * k:t * k + k]
        for j in range(k):
            x = shift_lst(long_word, j)
            key = ''
            for i in range(k):
                key += alphabet[(alphabet.index(y[i]) - alphabet.index(x[i])) % n]
            keys.append(key)
    writef('keys5_2.txt', {'keys': keys})
    # decs = dict()
    # key_index = 0
    # for key in keys:
    #     result = ''
    #     for char in enc_text:
    #         if char in alphabet:
    #             char_index = (alphabet.index(char) - alphabet.index(key[key_index])) % len(alphabet)
    #             result += alphabet[char_index]
    #             key_index = (key_index + 1) % k
    #         else:
    #             result += char
    #     decs[key] = result
    # writef('dec_text5.txt', decs)


print('Выберите действие: ')
print('0 - ввести ключ')
print('1 - получить алфавит открытого текста')
print('2 - зашифровать текст')
print('3 - вычислить частоты большого открытого текста')
print('4 - вычислить частоты шифротекста')
print('5 - атака по частотному анализу')
print('6 - вычислить частоты слов открытого текста')
print('7 - атака по вероятному слову')

while True:
    action = int(input('> введите номер действия '))
    if action == 0:
        with open('key5.txt', 'w') as f:
            f.write(input('Введите ключ '))
    elif action == 1:
        get_alphabet()
    elif action == 2:
        vigenere_cipher('encrypt')
    elif action == 3:
        frequency('big_text.txt')
    elif action == 4:
        frequency('enc_text.txt')
    elif action == 5:
        k = int(input('Введите длину ключа '))
        freq_attack(k)
    elif action == 6:
        word_freq()
    elif action == 7:
        k = int(input('Введите длину ключа '))
        word = input('Введите вероятное слово ')
        word_attack(k, word)
    else:
        break