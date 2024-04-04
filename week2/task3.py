import json
from random import shuffle
from itertools import permutations

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


def encrypt():
    key = readf("key1.txt")['k']
    k = len(key)
    key = key + [key[0]]

    with open("open_text.txt", "r", encoding='utf-8') as f:
        plaintext = f.read()

    f = open("enc_text.txt", 'w+')
    for i in range(len(plaintext) // k + 1):
        block = plaintext[i * k:(i + 1) * k]
        block = block + ' ' * (k - len(block))
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


def find_all_bigrams():
    with open("open_text.txt", 'r') as file:
        text = []
        for line in file:
            text.append(list(line.upper()))

    bigrams = set()
    for i in range(len(text)):
        for j in range(1, len(text[i])-1):
            bigrams.add(text[i][j-1] + text[i][j])

    writef("forbidden_bigrams.txt", {"bigrams": list(bigrams)})
    return bigrams


def get_alphabet():
    with open("open_text.txt", 'r') as file:
        text = file.read().upper()
        alphabet = ''.join(set(text))

    writef("alphabet.txt", {'alphabet': alphabet})
    return alphabet


def get_sup_table(k):
    bigrams = readf("forbidden_bigrams.txt")['bigrams']
    table = [['0'] * k for _ in range(k)]
    with open("enc_text.txt", 'r') as enc_file:
        enc = enc_file.read()[:k * k]

    enc = list(enc)
    enc_k = []
    for i in range(k):
        enc_k.append(enc[i:i + k])

    # for row in enc_k:
    #     print(row)
    # print(bigrams)

    for i in range(k - 1):
        for j in range(k):
            if enc_k[j][i] + enc_k[j][i + 1] in bigrams:
                print(enc_k[j][i] + enc_k[j][i + 1])
                table[i][j] = 'X'

    with open("sup_table.txt", 'w') as f:
        for row in table:
            f.write(''.join(row) + '\n')


# find_all_bigrams()
# get_alphabet()
k = 6
# gen_key(k)
# encrypt()
get_sup_table(k)