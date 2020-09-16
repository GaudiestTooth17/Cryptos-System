def mew(char):
    """
    ordinal value of char
    """
    return ord(char.lower()) - ord('a')


def mew_inverse(ord_value):
    """
    given an ordinal value, return the character
    """
    return chr(ord_value % 26 + ord('a'))


def chunk_plaintext(text, n):
    chunked_text = []
    for i in range(0, len(text), n):
        chunked_text.append(text[i:min(i+n, len(text))])
    return chunked_text


def mutate_key(key):
    print(f'old key: {key}')
    new_key = ''
    for c in key:
        new_key += mew_inverse(mew(c) + mew(key[-1]))
    print(f'new key: {new_key}')
    return new_key


def apply_key(text, key):
    encrypted_text = ''
    for i in range(min(len(text), len(key))):
        encrypted_text += mew_inverse(mew(text[i]) + mew(key[i]))
    return encrypted_text


def encrypt(plaintext, key):
    chunked_text = chunk_plaintext(plaintext, len(key)-1)
    cipher_text = ''
    for chunk in chunked_text:
        cipher_text += apply_key(chunk, key)
        key = mutate_key(key)
    return cipher_text


print(encrypt('cryptofun', 'code'))

# list_key = list(zip([chr(i + ord('a')) for i in range(26)], range(26)))
# for pair in list_key:
#     print(pair)
