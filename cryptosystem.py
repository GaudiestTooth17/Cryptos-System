import numpy as np
import math
import sys


def main():
    key = sys.argv[1]
    plain_text_file_name = sys.argv[2]
    with open(plain_text_file_name, 'r') as f:
        lines = f.readlines()
    plain_text = ''
    for line in lines:
        plain_text += line

    text_matrix = text_to_matrix(plain_text)
    key_matrix = key_to_matrix(key, text_matrix.shape[0])
    encrypted_matrix = np.matmul(key_matrix, text_matrix)
    cipher_text = matrix_to_text(encrypted_matrix)

    with open('encrypted_'+plain_text_file_name, 'w') as f:
        f.write(cipher_text)


def key_to_matrix(key: str, n: int) -> np.ndarray:
    """
    Creates an invertible matrix from the provided string.
    """
    key_matrix = np.identity(n)
    return key_matrix


def text_to_matrix(plain_text: str) -> np.ndarray:
    side_length = math.ceil(math.sqrt(len(plain_text)))
    text_matrix = np.zeros((side_length, side_length), dtype=np.uint32)

    text_index = 0
    for i in range(side_length):
        for j in range(side_length):
            text_matrix[i][j] = ord(plain_text[text_index])
            text_index += 1

    return text_matrix


def matrix_to_text(matrix: np.ndarray) -> str:
    text = ''
    for row in matrix:
        for num in row:
            text += num_to_str(num)


def num_to_str(num: int) -> str:
    return hex(num)[2:] + ' '


if __name__ == '__main__':
    main()
