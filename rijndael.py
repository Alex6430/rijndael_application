from fields import *


global rounds
global Nb, Nk, Nr, block_st, polynom
rounds = 10

def initialization(blok,key,poly):
    # global Nb, Nk, Nr, block_st, polynom
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
    #A = [0x8F, 0xC7, 0xE3, 0xF1, 0xF8, 0x7C, 0x3E, 0x1F]
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
                    new_state[i][j] = mult_element(c[i][k], state[k][j], 283)
                else:
                    new_state[i][j] ^= mult_element(c[i][k], state[k][j], 283)

    return new_state


def add_round_key(state, key):
    new_state = [[0 for i in range(Nb)] for i in range(4)]

    for i in range(4):
        for j in range(Nb):
            new_state[i][j] = add_sub(state[i][j], key[i][j])

    return new_state


def xor_element_mas(mas1, mas2):
    n = len(mas1)
    temp = [0]*n
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


# def key_expansion_128bits(key):
#     key_expan = [0]*44
#     rc = [0]*10
#     rc[0] = 0x01
#
#     for i in range(1, 10, 1):
#         rc[i] = mult_element(0x02, rc[i-1], 0x11B)
#
#     key_expan[0], key_expan[1], key_expan[2], key_expan[3] = key[0:4], key[4:8], key[8:12], key[12:16]
#     for i in range(0, 40, 4):
#         if i % 4 == 0:
#             key_expan[i+4] = xor_element_mas(key_expan[i], g(key_expan[i+3], rc[i//4]))
#         key_expan[i+5] = xor_element_mas(key_expan[i+4], key_expan[i+1])
#         key_expan[i+6] = xor_element_mas(key_expan[i+5], key_expan[i+2])
#         key_expan[i+7] = xor_element_mas(key_expan[i+6], key_expan[i+3])
#
#     return key_expan
#
#
# def key_expansion_192_256bits(key):
#     n = Nb*(Nr+1)
#     key_expan = [0]*n
#     rc = [0]*Nr
#     rc[0] = 0x01
#
#     for i in range(1, Nr, 1):
#         rc[i] = mult_element(0x02, rc[i-1], 0x11B)
#
#     for i in range(Nk):
#         key_expan[i] = key[4*i:4*i+4]
#
#     for i in range(Nk, n, 1):
#         if i % Nk == 0:
#             key_expan[i] = xor_element_mas(key_expan[i-Nk], g(key_expan[i-1], rc[i//Nk]))
#         elif i % Nk == 4:
#             key_expan[i] = xor_element_mas(sub_word(key_expan[i-1]), key_expan[i-Nk])
#         else:
#             key_expan[i] = xor_element_mas(key_expan[i-Nk], key_expan[i-1])
#
#     return key_expan
#
#
def sub_word(w):
    s_boxes = init_s()
    s = s_boxes[0]

    new_w = [0]*4
    for i in range(4):
        new_w[i] = s[w[i]]

    return new_w


def key_expansion(str_key):
    key = [0] * len(str_key)
    for i in range(len(str_key)):
        key[i] = ord(str_key[i])

    n = Nb * (Nr + 1)
    key_expan = [0]*n

    rc = [0] * Nr
    rc[0] = 0x01

    for i in range(1, Nr, 1):
        rc[i] = mult_element(0x02, rc[i - 1], 0x11B)

    for i in range(n):
        if i < Nk:
            key_expan[i] = key[4*i:4*i+4]
        elif i >= Nk and i % Nk == 0:
            key_expan[i] = xor_element_mas(key_expan[i-Nk], g(key_expan[i-1], rc[i//Nk-1]))
        elif i >= Nk and Nk > 6 and i % Nk == 4:
            key_expan[i] = xor_element_mas(key_expan[i-Nk], sub_word(key_expan[i-1]))
        else:
            key_expan[i] = xor_element_mas(key_expan[i-Nk], key_expan[i-1])

    return key_expan


def transformation(str):
    Nb = len(str) // 4
    new_str = [0]*len(str)
    for i in range(len(str)):
        new_str[i] = ord(str[i])

    mas = [[0 for i in range(Nb)] for i in range(4)]

    for i in range(Nb):
        w = new_str[4*i:4*i+4]
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
        round_key = key_transform(expanded_key[Nb*i:Nb*(i+1)])
        encrypt_state = add_round_key(encrypt_state, round_key)

    encrypt_state = byte_sub(encrypt_state)
    encrypt_state = shift_row(encrypt_state)
    round_key = key_transform(expanded_key[Nb*Nr:Nb*(Nr+1)])
    encrypt_state = add_round_key(encrypt_state, round_key)

    return encrypt_state


def decryption(decrypt_state, str_key):
    decrypt_state = transformation(decrypt_state)
    expanded_key = key_expansion(str_key)
    state = add_round_key(decrypt_state, key_transform(expanded_key[Nb*Nr:Nb*(Nr+1)]))

    for i in range(Nr-1, 0, -1):
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


#global Nb, Nk, Nr
#Nb = 8
#Nk = 8
#Nr = max(Nb, Nk) + 6


def to_string(state):
    mas = []
    for i in range(Nb):
        for j in range(4):
            mas.append(state[j][i])

    str =''
    for i in range(len(mas)):
        str += chr(mas[i])

    return str


key = "Thats my Kung Fu Two One Nine Tw"
state = "Two One Nine Two Two One Nine Tw"
# key = key_expansion(key)
# round_key = key_transform(key[0:6])
# st = transformation(state)
# st1 = add_round_key(st, round_key)
# st2 = byte_sub(st1)
# st3 = shift_row(st2)
# st4 = mix_columns(st3)
# print(st4)

# decrypt = rijndael(state, key)
# print(decrypt)
# mas = to_string(decrypt)
# print(mas)
# encrypt = decryption(mas, key)
# print(encrypt)
# mas = to_string(encrypt)
# print(mas)

#state = [[0x54, 0x4F, 0x4E, 0x20],
#         [0x77, 0x6E, 0x69, 0x54],
#         [0x6F, 0x65, 0x6E, 0x77],
#         [0x20, 0x20, 0x65, 0x6F]]

#key = [[0x54, 0x73, 0x20, 0x67],
#       [0x68, 0x20, 0x4B, 0x20],
#       [0x61, 0x6D, 0x75, 0x46],
#       [0x74, 0x79, 0x6E, 0x75]]