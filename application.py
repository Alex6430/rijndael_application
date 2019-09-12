from fields import *
# global Nb, Nk, Nr, block_st, polynom


def encryptRijndael(filename, mode, key, IV):
    print(filename)
    print(mode)
    print(key)
    print(IV)
    print(block_st)
    print(Nb)
    print(Nk)
    print(Nr)
    print(polynom)
    state = read_file_in_state(filename, block_st)
    print(state)
    if mode == 1:
        encrypt_msg = electronic_code_book_encrypt(state, key)
    elif mode == 2:
        encrypt_msg = cipher_block_chaining_encrypt(state, key, IV)
    elif mode == 3:
        encrypt_msg = output_feedback_encrypt(state, key, IV)
    elif mode == 4:
        encrypt_msg = ciper_feedback_encrypt(state, key, IV)
    print("сработал encript")
    file_encrypt = name_file_encrypt(filename)
    write_in_file(file_encrypt, encrypt_msg)


def decryptRijndael(filename, mode, key, IV):
    state = read_file_in_state(filename, block_st)
    if mode == 1:
        decrypt_msg = electronic_code_book_decrypt(state, key)
    elif mode == 2:
        decrypt_msg = cipher_block_chaining_decrypt(state, key, IV)
    elif mode == 3:
        decrypt_msg = output_feedback_decrypt(state, key, IV)
    elif mode == 4:
        decrypt_msg = ciper_feedback_decrypt(state, key, IV)

    file_decrypt = name_file_decrypt(filename)
    write_in_file(file_decrypt, decrypt_msg)


def read_file_in_state(filename, size_block):
    with open(filename, 'r', encoding="utf-8") as filehandle:
        filecontent = filehandle.read()
        # print(filecontent)
    filecontent = filecontent.replace('\q', "\r")
    size_state = len(filecontent) // size_block
    if not len(filecontent) % size_block == 0:
        size_state += 1
    state = [0] * size_state
    for i in range(size_state):
        data = filecontent[size_block * i:size_block * (i + 1)]
        str = ""
        for j in range(len(data)):
            str += data[j]
        if i == size_state - 1:
            if not size_block - len(data) == 0:
                for k in range(size_block - len(data)):
                    str += " "
        state[i] = str
        # print(state[i])
        # print("/--/--/--/--/--/--/--/--/--/--/--/--/")

    return state


def read_file_in_key(filename):
    with open(filename, 'r', encoding="utf-8") as filehandle:
        filecontent = filehandle.read()
        # print(filecontent)

    str = ""
    for i in range(len(filecontent)):
        str += filecontent[i]

    return str


def write_in_file(filename, state):
    with open(filename, 'w', encoding="utf-8") as filehandle:
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == '\r':
                    filehandle.write('\q')
                else:
                    filehandle.write(state[i][j])


def name_file_encrypt(filename):
    print(filename)
    n = len(filename)
    str = filename[0: n - 4] + "encrypt" + filename[n - 4: n]
    return str


def name_file_decrypt(filename):
    index = filename.find("encrypt")
    # print(index)
    if not index == -1:
        filename = filename[0: len(filename) - 11] + ".txt"

    n = len(filename)
    str = filename[0: n - 4] + "decrypt" + filename[n - 4: n]
    return str


def electronic_code_book_encrypt(mas, key):
    # key = "Thats my Kung Fu"
    # state1 = "Two One Nine Two"
    # state2 = "One Nine Two Two"
    # state3 = "Nine Two Two One"
    # state4 = "Two Two One Nine"

    # mas = [state1, state2, state3, state4]

    encrypt_msg = [0] * len(mas)

    for i in range(len(mas)):
        encrypt_msg[i] = to_string(rijndael(mas[i], key))
        # print(to_string(encrypt_msg[i]))

    return encrypt_msg


def electronic_code_book_decrypt(encrypt_msg, key):
    decrypt_msg = [0] * len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        decrypt_msg[i] = to_string(decryption(encrypt_msg[i], key))
        # print(to_string(decrypt_msg[i]))

    return decrypt_msg


def xor_str(str1, str2):
    mas_str1 = [0] * len(str1)
    mas_str2 = [0] * len(str1)
    mas_str = [0] * len(str1)
    for i in range(len(str1)):
        mas_str1[i] = ord(str1[i])
        mas_str2[i] = ord(str2[i])

    mas_str = xor_element_mas(mas_str1, mas_str2)

    str = ''
    for i in range(len(mas_str)):
        str += chr(mas_str[i])
    return str


def cipher_block_chaining_encrypt(mas, key, IV):
    # IV = "Thats my Kung Fu"
    # key = "Thats my Kung Fu"
    # state1 = "Two One Nine Two"
    # state2 = "One Nine Two Two"
    # state3 = "Nine Two Two One"
    # state4 = "Two Two One Nine"
    #
    # mas = [state1, state2, state3, state4]

    encrypt_msg = [0] * len(mas)

    for i in range(len(mas)):
        if i == 0:
            state = xor_str(mas[0], IV)
            encrypt_msg[i] = to_string(rijndael(state, key))
        else:
            state = xor_str(mas[i], encrypt_msg[i - 1])
            encrypt_msg[i] = to_string(rijndael(state, key))
        # print(encrypt_msg[i])

    return encrypt_msg


def cipher_block_chaining_decrypt(encrypt_msg, key, IV):
    # IV = "Thats my Kung Fu"

    decrypt_str = [0] * len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        if i == 0:
            state = to_string(decryption(encrypt_msg[i], key))
            decrypt_str[i] = xor_str(state, IV)
        else:
            state = to_string(decryption(encrypt_msg[i], key))
            decrypt_str[i] = xor_str(state, encrypt_msg[i - 1])
        # print(decrypt_str[i])

    return decrypt_str


def output_feedback_encrypt(mas, key, IV):
    # IV = "Thats my Kung Fu"
    # key = "Thats my Kung Fu"

    # state1 = "Two One Nine Two"
    # state2 = "One Nine Two Two"
    # state3 = "Nine Two Two One"
    # state4 = "Two Two One Nine"
    #
    # mas = [state1, state2, state3, state4]

    encrypt_msg = [0] * len(mas)

    x = IV

    for i in range(len(mas)):
        if i == 0:
            y = to_string(rijndael(IV, key))
            encrypt_msg[i] = xor_str(mas[i], y)
            x = y
        else:
            y = to_string(rijndael(x, key))
            encrypt_msg[i] = xor_str(mas[i], y)
            x = y
        # print(encrypt_msg[i])

    return encrypt_msg


def output_feedback_decrypt(encrypt_msg, key, IV):
    # IV = "Thats my Kung Fu"

    decrypt_msg = [0] * len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        if i == 0:
            y = to_string(rijndael(IV, key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
            x = y
        else:
            y = to_string(rijndael(x, key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
            x = y
        # print(decrypt_msg[i])

    return decrypt_msg


def ciper_feedback_encrypt(mas, key, IV):
    # IV = "Thats my Kung Fu Nine Two Nine Tw"
    # key = "Thats my Kung Fu"
    #
    # state1 = "Two One Nine Two"
    # state2 = "One Nine Two Two"
    # state3 = "Nine Two Two One"
    # state4 = "Two Two One Nine"
    #
    # mas = [state1, state2, state3, state4]

    encrypt_msg = [0] * len(mas)

    for i in range(len(mas)):
        if i == 0:
            y = to_string(rijndael(IV, key))
            encrypt_msg[i] = xor_str(mas[i], y)
        else:
            y = to_string(rijndael(encrypt_msg[i - 1], key))
            encrypt_msg[i] = xor_str(mas[i], y)
        # print(encrypt_msg[i])

    return encrypt_msg


def ciper_feedback_decrypt(encrypt_msg, key, IV):
    # IV = "Thats my Kung Fu Nine Two Nine Tw"

    decrypt_msg = [0] * len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        if i == 0:
            y = to_string(rijndael(IV, key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
        else:
            y = to_string(rijndael(encrypt_msg[i - 1], key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
        # print(decrypt_msg[i])

    return decrypt_msg


def initialization(blok, key, poly):
    global Nb, Nk, Nr, block_st, polynom
    Nb = blok // 32
    Nk = key // 32
    Nr = max(Nb, Nk) + 6
    block_st = blok // 8
    polynom = poly
    print(block_st)
    print(Nb)
    print(Nk)
    print(Nr)
    print(polynom)


def xor(x, length):
    length = length >> 1
    while length:
        x = ((x >> length) ^ x & ((1 << length) - 1))
        length = length >> 1
    return x


def affine_transformation(x):
    # A = [0x8F, 0xC7, 0xE3, 0xF1, 0xF8, 0x7C, 0x3E, 0x1F]
    A = [0xF8, 0x7C, 0x3E, 0x1F, 0x8F, 0xC7, 0xE3, 0xF1]
    result = 0
    i = 0
    while i < 8:
        result = (result << 1) + xor(A[i] & x, 8)
        i += 1

    return result ^ 0x63


def init_s():
    s = [0] * 256
    s_inverse = [0] * 256
    for i in range(256):
        s[i] = affine_transformation(extandEuclid(i, 283))
    for i in range(256):
        s_inverse[s[i]] = i

    return s, s_inverse


def byte_sub(state, inverse=False):
    s_boxes = init_s()
    s = s_boxes[0]
    s_inverse = s_boxes[1]

    new_state = [[0 for i in range(Nb)] for i in range(4)]

    if not inverse:
        for i in range(4):
            for j in range(Nb):
                new_state[i][j] = s[state[i][j]]
    else:
        for i in range(4):
            for j in range(Nb):
                new_state[i][j] = s_inverse[state[i][j]]

    return new_state


def move_left(x, pos):
    return x[pos:] + x[:pos]


def move_right(x, pos):
    return x[-pos:] + x[:-pos]


def shift_row(state, inverse=False):
    new_state = [[0 for i in range(Nb)] for i in range(4)]

    if not inverse:

        for i in range(4):
            new_state[i] = move_left(state[i], i)
    else:
        for i in range(4):
            new_state[i] = move_right(state[i], i)

    return new_state


def mix_columns(state, inverse=False):
    c = [[0 for i in range(4)] for i in range(4)]

    new_state = [[0 for i in range(Nb)] for i in range(4)]

    if not inverse:
        c = [[0x02, 0x03, 0x01, 0x01],
             [0x01, 0x02, 0x03, 0x01],
             [0x01, 0x01, 0x02, 0x03],
             [0x03, 0x01, 0x01, 0x02]]
    else:
        c = [[0x0E, 0x0B, 0x0D, 0x09],
             [0x09, 0x0E, 0x0B, 0x0D],
             [0x0D, 0x09, 0x0E, 0x0B],
             [0x0B, 0x0D, 0x09, 0x0E]]

    for i in range(4):
        for j in range(Nb):
            for k in range(4):
                if k == 0:
                    new_state[i][j] = mult_element(c[i][k], state[k][j], polynom)
                else:
                    new_state[i][j] ^= mult_element(c[i][k], state[k][j], polynom)

    return new_state


def add_round_key(state, key):
    new_state = [[0 for i in range(Nb)] for i in range(4)]

    for i in range(4):
        for j in range(Nb):
            new_state[i][j] = add_sub(state[i][j], key[i][j])

    return new_state


def xor_element_mas(mas1, mas2):
    n = len(mas1)
    temp = [0] * n
    for i in range(n):
        temp[i] = mas1[i] ^ mas2[i]

    return temp


def g(w, rc):
    s_boxes = init_s()
    s = s_boxes[0]

    r_con = [rc, 0x00, 0x00, 0x00]

    w_new = move_left(w, 1)
    for i in range(4):
        w_new[i] = s[w_new[i]]

    key = xor_element_mas(w_new, r_con)

    return key


def sub_word(w):
    s_boxes = init_s()
    s = s_boxes[0]

    new_w = [0] * 4
    for i in range(4):
        new_w[i] = s[w[i]]

    return new_w


def key_expansion(str_key):
    key = [0] * len(str_key)
    for i in range(len(str_key)):
        key[i] = ord(str_key[i])

    n = Nb * (Nr + 1)
    key_expan = [0] * n

    rc = [0] * 30
    rc[0] = 0x01

    for i in range(1, 30, 1):
        rc[i] = mult_element(0x02, rc[i - 1], polynom)

    for i in range(n):
        if i < Nk:
            key_expan[i] = key[4 * i:4 * i + 4]
        elif i >= Nk and i % Nk == 0:
            key_expan[i] = xor_element_mas(key_expan[i - Nk], g(key_expan[i - 1], rc[i // Nk - 1]))
        elif i >= Nk and Nk > 6 and i % Nk == 4:
            key_expan[i] = xor_element_mas(key_expan[i - Nk], sub_word(key_expan[i - 1]))
        else:
            key_expan[i] = xor_element_mas(key_expan[i - Nk], key_expan[i - 1])

    return key_expan


def transformation(str):
    Nb = len(str) // 4
    new_str = [0] * len(str)
    for i in range(len(str)):
        new_str[i] = ord(str[i])

    mas = [[0 for i in range(Nb)] for i in range(4)]

    for i in range(Nb):
        w = new_str[4 * i:4 * i + 4]
        mas[0][i] = w[0]
        mas[1][i] = w[1]
        mas[2][i] = w[2]
        mas[3][i] = w[3]

    return mas


def key_transform(round_key):
    key = [[0 for i in range(Nb)] for i in range(4)]

    for i in range(4):
        for j in range(Nb):
            key[i][j] = round_key[j][i]

    return key


def rijndael(state, str_key):
    state = transformation(state)
    expanded_key = key_expansion(str_key)
    encrypt_state = add_round_key(state, key_transform(expanded_key[0:Nb]))

    for i in range(1, Nr, 1):
        encrypt_state = byte_sub(encrypt_state)
        encrypt_state = shift_row(encrypt_state)
        encrypt_state = mix_columns(encrypt_state)
        round_key = key_transform(expanded_key[Nb * i:Nb * (i + 1)])
        encrypt_state = add_round_key(encrypt_state, round_key)

    encrypt_state = byte_sub(encrypt_state)
    encrypt_state = shift_row(encrypt_state)
    round_key = key_transform(expanded_key[Nb * Nr:Nb * (Nr + 1)])
    encrypt_state = add_round_key(encrypt_state, round_key)

    return encrypt_state


def decryption(decrypt_state, str_key):
    decrypt_state = transformation(decrypt_state)
    expanded_key = key_expansion(str_key)
    state = add_round_key(decrypt_state, key_transform(expanded_key[Nb * Nr:Nb * (Nr + 1)]))

    for i in range(Nr - 1, 0, -1):
        state = shift_row(state, True)
        state = byte_sub(state, True)
        round_key = key_transform(expanded_key[Nb * i:Nb * (i + 1)])
        state = add_round_key(state, round_key)
        state = mix_columns(state, True)

    state = shift_row(state, True)
    state = byte_sub(state, True)
    round_key = key_transform(expanded_key[0:Nb])
    state = add_round_key(state, round_key)

    return state


# global Nb, Nk, Nr
# Nb = 8
# Nk = 8
# Nr = max(Nb, Nk) + 6


def to_string(state):
    mas = []
    for i in range(Nb):
        for j in range(4):
            mas.append(state[j][i])

    str = ''
    for i in range(len(mas)):
        str += chr(mas[i])

    return str
