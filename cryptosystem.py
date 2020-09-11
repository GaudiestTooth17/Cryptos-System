import numpy as np
import math
import sys
from typing import List
import itertools


def main():
    mode = sys.argv[1]
    key = sys.argv[2]
    file_name = sys.argv[3]
    if mode == 'e':
        encrypt(file_name, key)
    elif mode == 'd':
        decrypt(file_name, key)
    else:
        print(f'Unrecognized mode {mode}.')


def encrypt(file_name: str, key: str) -> None:
    with open(file_name, 'r') as f:
        lines = f.readlines()
    plain_text = ''
    for line in lines:
        plain_text += line

    text_matrix = text_to_matrix(plain_text)
    key_matrix = key_to_matrix(key, text_matrix.shape[0])
    encrypted_matrix = np.matmul(key_matrix, text_matrix)
    # print(matrix_to_plain_text(encrypted_matrix))
    cipher_text = matrix_to_text(encrypted_matrix)

    with open('encrypted_'+file_name, 'w') as f:
        f.write(cipher_text)


def decrypt(file_name: str, key: str) -> None:
    with open(file_name, 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        while lines[i][-1] == '\n':
            lines[i] = lines[i][:-1]
    entries = ''.join(lines).split(' ')

    encrypted_matrix = entries_to_matrix(entries)
    key_matrix = np.linalg.inv(key_to_matrix(key, encrypted_matrix.shape[0]))
    decrypted_matrix = np.matmul(key_matrix, encrypted_matrix)
    plain_text = matrix_to_plain_text(decrypted_matrix)

    with open('decrypted_'+file_name, 'w') as f:
        f.write(plain_text)


def entries_to_matrix(entries: List[str]) -> np.ndarray:
    n = int(math.sqrt(len(entries)))
    matrix = np.zeros((n, n), dtype=np.uint32)

    index = 0
    for i in range(n):
        for j in range(n):
            matrix[i][j] = int(entries[index], 16)
            index += 1

    return matrix


def matrix_to_plain_text(matrix: np.ndarray) -> str:
    text = ''
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            print(matrix[i][j])
            text += chr(matrix[i][j])
    return text


def key_to_matrix(key: str, n: int) -> np.ndarray:
    """
    Creates an invertible matrix from the provided string.
    """
    key_matrix = np.identity(n, dtype=np.uint32)

    new_key = ''
    for i in range(n):
        new_key += key[i % len(key)]

    for i, key_element in enumerate(new_key):
        key_matrix[i] *= ord(key_element) % 32

    for i in range(0, len(new_key)-1, 2):
        print(new_key[i:i+2])
        row1, row2, x = substring_to_numbers(new_key[i:i+2], n)
        key_matrix[row1] += (x % 32) * key_matrix[row2]

    return key_matrix


def substring_to_numbers(sub_str: str, n: int):
    """
    Substring should contain two characters
    :return: Two numbers in range(n)
    """
    num1 = ord(sub_str[0]) % n
    num2 = (5 * ord(sub_str[1])) % n
    num3 = (ord(sub_str[0]) + ord(sub_str[1])) % n
    print((num1, num2, num3))
    return num1, num2, num3


def text_to_matrix(plain_text: str) -> np.ndarray:
    side_length = math.ceil(math.sqrt(len(plain_text)))
    text_matrix = np.zeros((side_length, side_length), dtype=np.uint32)
    # make the text have as many symbols as the array has elements
    padded_text = plain_text + ''.join(['~' for _ in range(side_length ** 2 - len(plain_text))])

    text_index = 0
    for i in range(side_length):
        for j in range(side_length):
            text_matrix[i][j] = ord(padded_text[text_index])
            text_index += 1

    return text_matrix


def matrix_to_text(matrix: np.ndarray) -> str:
    text = ''
    for row in matrix:
        for num in row:
            text += num_to_str(num)
    return text


def num_to_str(num: int) -> str:
    return hex(num)[2:] + ' '


if __name__ == '__main__':
    main()
