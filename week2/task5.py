# -*- coding: utf-8 -*-
import json


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


# def get_alphabet2(text):
#     alphabet = ''.join(sorted(list(set(text))))
#
#     return alphabet


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


# get_alphabet()
# frequency('big_text.txt')
# vigenere_cipher('encrypt')
freq_attack(7)