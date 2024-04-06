import json
from random import shuffle
from itertools import permutations, combinations_with_replacement

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
        f.write('\n' + str(key[:-1 ]) + ":\n    ")
        for i in range(len(plaintext) // k + 1):
            enc_block = plaintext[i * k:(i + 1) * k]
            block = [""] * k
            for j in range(len(enc_block)):
                block[key[j + 1]] = enc_block[key[j]]
            f.write(''.join(block))

    f.close()

def get_alphabet():
    with open("open_text.txt", 'r', encoding='utf-8') as file:
        text = file.read().upper()
        alphabet = ''.join(set(text))

    writef("alphabet.txt", {'alphabet': alphabet})
    return alphabet


def find_forbidden_bigrams():
    alphabet = readf('alphabet.txt')['alphabet']
    all_bigrams = set()
    for a, b in combinations_with_replacement(alphabet, 2):
        all_bigrams.add(a + b)
    forbidden_bigrams = all_bigrams - find_all_bigrams_in_text()
    writef('forbidden_bigrams.txt', {'bigrams' : list(forbidden_bigrams)})


def find_all_bigrams_in_text():
    with open("open_text.txt", 'r', encoding='utf-8') as file:
        text = []
        for line in file:
            text.append(list(line.upper()))

    bigrams = set()
    for i in range(len(text)):
        for j in range(1, len(text[i])-1):
            bigrams.add(text[i][j-1] + text[i][j])

    return bigrams


def get_sup_table(k):
    bigrams = readf("forbidden_bigrams.txt")['bigrams']
    table = [['0'] * k for _ in range(k)]
    with open("enc_text.txt", 'r') as enc_file:
        enc = enc_file.read().upper()

    enc = list(enc)
    enc_k = []
    for j in range(len(enc) // k):
        enc_k.append(enc[j:j + k])

    for row in range(k):
        print(enc_k[row])
    # print(bigrams)
    for i in range(k):
        for j in range(k):
            for l in range(k):
                if i == j or (enc_k[l][i] + enc_k[l][j] in bigrams):
                    # print(i + 1, j + 1, l + 1, enc_k[l][i] + enc_k[l][j])
                    table[i][j] = 'X'
                    # for row in table:
                    #     print(''.join(row))

    print('Вспомогательная таблица:')
    with open("sup_table.txt", 'w') as f:
        for row in table:
            print(''.join(row))
            f.write(''.join(row) + '\n')


def get_keys_tree():
    pass


k = 5
# get_alphabet()
# find_forbidden_bigrams()
# gen_key(k)
# encrypt()
get_sup_table(k)
decrypt(k)