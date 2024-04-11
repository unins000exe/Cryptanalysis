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
        alphabet = ''.join(set(text))

    writef("alphabet.txt", {'alphabet': alphabet})
    return alphabet


def shift_lst(lst, sh):
    return lst[-sh:] + lst[:-sh]


def enter_key():
    key = int(input('Введите ключ - номер сдвига алфавита '))

    alphabet = readf('alphabet.txt')['alphabet']
    shift_alph = shift_lst(alphabet, key)

    writef('key4.txt', {'shift': shift_alph})


def encrypt():
    alphabet = readf('alphabet.txt')['alphabet']
    shift = readf('key4.txt')['shift']
    n = len(alphabet)

    alph_num = dict(zip(alphabet.upper(), [i for i in range(n)]))
    num_shift = dict(zip([i for i in range(n)], shift))
    print(alph_num)
    print(num_shift)

    with open('open_text.txt', 'r', encoding='utf-8') as f:
        open_text = f.read()

    with open('enc_text.txt', 'w+', encoding='utf-8') as f:
        for c in open_text:
            f.write(num_shift[alph_num[c.upper()]])


def frequency(file):
    alphabet = readf('alphabet.txt')['alphabet']
    freq = dict(zip(alphabet, [0] * len(alphabet)))
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read().upper()
        n = len(text)
        for c in text:
            if c in freq.keys():
                freq[c] += 1

    for c in freq:
        freq[c] /= n

    freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    writef('freq_' + file + '.txt', freq)


def isotonic_maps():
    alphabet = readf('alphabet.txt')['alphabet']
    shift = readf('key4.txt')['shift']
    freq_big_text = readf('freq_big_text.txt.txt')
    freq_enc_text = readf('freq_enc_text.txt.txt')

    n = len(alphabet)
    alph_num = dict(zip(alphabet.upper(), [i for i in range(n)]))
    keys = []

    freq_lst_bt = list(freq_big_text.keys())
    freq_lst_et = list(freq_enc_text.keys())
    for i in range(n):
        key = dict(zip(freq_lst_bt, shift_lst(freq_lst_et, -i)))
        keys.append(key)
    writef('keys4.txt', {'keys': keys})

def try_encrypt():
    pass


# get_alphabet()
# enter_key()
# encrypt()
# frequency('big_text.txt')
# frequency('enc_text.txt')
isotonic_maps()
