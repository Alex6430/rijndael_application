from rijndael import *

def electronic_code_book_encrypt(mas, key):
    #key = "Thats my Kung Fu"
    # state1 = "Two One Nine Two"
    # state2 = "One Nine Two Two"
    # state3 = "Nine Two Two One"
    # state4 = "Two Two One Nine"

    #mas = [state1, state2, state3, state4]

    encrypt_msg = [0]*len(mas)

    for i in range(len(mas)):
        encrypt_msg[i] = to_string(rijndael(mas[i], key))
        #print(to_string(encrypt_msg[i]))

    return encrypt_msg


def electronic_code_book_decrypt(encrypt_msg, key):

    decrypt_msg = [0]*len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        decrypt_msg[i] = to_string(decryption(encrypt_msg[i], key))
        #print(to_string(decrypt_msg[i]))

    return decrypt_msg


def xor_str(str1, str2):
    mas_str1 = [0] * len(str1)
    mas_str2 = [0] * len(str1)
    mas_str = [0]*len(str1)
    for i in range(len(str1)):
        mas_str1[i] = ord(str1[i])
        mas_str2[i] = ord(str2[i])

    mas_str = xor_element_mas(mas_str1, mas_str2)

    str = ''
    for i in range(len(mas_str)):
        str += chr(mas_str[i])
    return str

def cipher_block_chaining_encrypt(mas, key, IV):
    #IV = "Thats my Kung Fu"
    #key = "Thats my Kung Fu"
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
            state = xor_str(mas[i], encrypt_msg[i-1])
            encrypt_msg[i] = to_string(rijndael(state, key))
        #print(encrypt_msg[i])

    return encrypt_msg


def cipher_block_chaining_decrypt(encrypt_msg, key, IV):
    #IV = "Thats my Kung Fu"

    decrypt_str = [0] * len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        if i == 0:
            state = to_string(decryption(encrypt_msg[i], key))
            decrypt_str[i] = xor_str(state, IV)
        else:
            state = to_string(decryption(encrypt_msg[i], key))
            decrypt_str[i] = xor_str(state, encrypt_msg[i-1])
        #print(decrypt_str[i])

    return decrypt_str


def output_feedback_encrypt(mas, key, IV):
    #IV = "Thats my Kung Fu"
    #key = "Thats my Kung Fu"

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
        #print(encrypt_msg[i])

    return encrypt_msg


def output_feedback_decrypt(encrypt_msg, key, IV):
    #IV = "Thats my Kung Fu"

    decrypt_msg = [0]*len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        if i == 0:
            y = to_string(rijndael(IV, key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
            x = y
        else:
            y = to_string(rijndael(x, key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
            x = y
        #print(decrypt_msg[i])

    return decrypt_msg


def ciper_feedback_encrypt(mas, key, IV):
    #IV = "Thats my Kung Fu Nine Two Nine Tw"
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
            y = to_string(rijndael(encrypt_msg[i-1], key))
            encrypt_msg[i] = xor_str(mas[i], y)
        #print(encrypt_msg[i])

    return encrypt_msg



def ciper_feedback_decrypt(encrypt_msg, key, IV):
    #IV = "Thats my Kung Fu Nine Two Nine Tw"

    decrypt_msg = [0]*len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        if i == 0:
            y = to_string(rijndael(IV, key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
        else:
            y = to_string(rijndael(encrypt_msg[i-1], key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
        #print(decrypt_msg[i])

    return decrypt_msg


#electronic_code_book()
#cipher_block_chaining()
#output_feedback()
#ciper_deedback()