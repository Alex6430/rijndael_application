import os
from cipher_mode import *
import string


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
        #print(state[i])
        #print("/--/--/--/--/--/--/--/--/--/--/--/--/")

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
                if state[i][j]=='\r':
                    filehandle.write('\q')
                else:
                    filehandle.write(state[i][j])


def name_file_encrypt(filename):
    print(filename)
    n = len(filename)
    str = filename[0: n-4] + "encrypt" + filename[n-4 : n]
    return str


def name_file_decrypt(filename):
    index = filename.find("encrypt")
    #print(index)
    if not index == -1:
        filename = filename[0 : len(filename) - 11] + ".txt"

    n = len(filename)
    str = filename[0: n - 4] + "decrypt" + filename[n - 4: n]
    return str

# filename = "text.txt"
# new_file = name_file_encrypt(filename)
# print(new_file)
# print(name_file_decrypt(new_file))

#global size_block
#size_block = 32

# filename1 = "text"
# state = read_file_in_state(filename1)
# filename2 = "key"
# key = read_file_in_key(filename2)
#
# encrypt_msg = ciper_feedback_encrypt(state, key)
# print(encrypt_msg)
# write_in_file("text1", encrypt_msg)
#
# state = read_file_in_state("text1")
# decrypt_msg = ciper_feedback_decrypt(encrypt_msg, key)
# print(decrypt_msg)
# write_in_file("text2", decrypt_msg)

#write_in_file("text2", decrypt_msg)
# print(decrypt_msg)
#cipher_block_chaining(state, key)
#output_feedback(state, key)
#ciper_deedback(state, key)