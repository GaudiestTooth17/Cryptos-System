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
    # swap two rows of the matrix
    row1, row2 = substring_to_numbers(key[:2])
    key_matrix[row1], key_matrix[row2] = key_matrix[row2], key_matrix[row1]

    # multiply row
    row, factor = substring_to_numbers(key[2:4])
    key_matrix[row] *= factor

    # swap rows
    row1, row2 = substring_to_numbers(key[4:6])
    key_matrix[row1], key_matrix[row2] = key_matrix[row2], key_matrix[row1]

    # add two rows
    row1, row2 = substring_to_numbers(key[6:8])
    key_matrix[row1] += key_matrix[row2]

    # multiply row
    row, factor = substring_to_numbers(key[8:10])
    key_matrix[row] *= factor

    return key_matrix


def substring_to_numbers(sub_str: str, n: int):
    """
    Substring should contain two characters
    :return: Two numbers in range(n)
    """
    num1 = (3 * ord(sub_str[0])) % n
    num2 = (5 * ord(sub_str[1])) % n
    return num1, num2


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
