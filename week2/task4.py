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

    alph_num = dict(zip(alphabet, [i for i in range(n)]))
    num_shift = dict(zip([i for i in range(n)], shift))
    print(alph_num)
    print(num_shift)

    with open('open_text.txt', 'r', encoding='utf-8') as f:
        open_text = f.read()

    with open('enc_text.txt', 'w+', encoding='utf-8') as f:
        for c in open_text:
            f.write(num_shift[alph_num[c]])


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

    writef('freq_' + file + '.txt', freq)


def isotonic_maps():
    alphabet = readf('alphabet.txt')['alphabet']
    freq_big_text = readf('freq_big_text.txt.txt')
    freq_enc_text = readf('freq_enc_text.txt.txt')

    n = len(alphabet)
    keys = []

    # freq_lst_bt = list(freq_big_text.keys())
    most = list(freq_big_text.keys())[0]
    freq_lst_et = list(freq_enc_text.keys())
    for i in range(n):
        sh = (alphabet.index(freq_lst_et[i]) - alphabet.index(most)) % n
        keys.append(shift_lst(alphabet, (sh - n) % n))

    writef('keys4.txt', {'keys': keys})


def try_decrypt():
    keys = readf('keys4.txt')['keys']

    alphabet = readf('alphabet.txt')['alphabet']
    n = len(alphabet)
    alph_num = dict(zip(alphabet, [i for i in range(n)]))

    with open('enc_text.txt', 'r', encoding='utf-8') as f:
        enc_text = f.read()

    with open('dec_text.txt', 'w+', encoding='utf-8') as f:
        for key in keys:
            num_shift = dict(zip([i for i in range(n)], key))
            f.write('\n==========================================================\n')
            f.write('Ключ + ' + str(key))
            for c in enc_text:
                f.write(num_shift[alph_num[c]])



#
#
#
#
#
#


print('Выберите действие: ')
print('0 - получить алфавит открытого текста')
print('1 - сгенерировать ключ (сдвиг) шифрования')
print('2 - зашифровать текст')
print('3 - вычислить частоты большого открытого текста')
print('4 - вычислить частоты шифротекста')
print('5 - построить возможные ключи')
print('6 - попытаться расшифровать')

while True:
    action = int(input('> введите номер действия '))
    if action == 0:
        get_alphabet()
    elif action == 1:
        enter_key()
    elif action == 2:
        encrypt()
    elif action == 3:
        frequency('big_text.txt')
    elif action == 4:
        frequency('enc_text.txt')
    elif action == 5:
        isotonic_maps()
    elif action == 6:
        try_decrypt()
    else:
        break
