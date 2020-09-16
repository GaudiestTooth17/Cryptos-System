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
    # print(f'old key: {key}')
    new_key = ''
    for c in key:
        new_key += mew_inverse(mew(c) + mew(key[-1]))
    # print(f'new key: {new_key}')
    return new_key


def apply_key(text, key):
    encrypted_text = ''
    for i in range(min(len(text), len(key))):
        encrypted_text += mew_inverse(mew(text[i]) + mew(key[i]))
    return encrypted_text


def remove_spaces(string):
    return ''.join(string.split(' '))


def reinsert_spaces(plaintext, cipher_text):
    words = plaintext.split(' ')
    # print(words)
    new_text = ''
    i = 0
    for word in words:
        new_text += cipher_text[i:i+len(word)] + ' '
        i += len(word)

    return new_text[:-1]


def remove_symbols(string):
    string = string.replace(',', '')
    string = string.replace('.', '')
    string = string.replace('—', '')
    string = string.replace('-', '')
    string = string.replace('\n', ' ')
    return string


def encrypt(plaintext, key):
    plaintext = remove_symbols(plaintext)
    # print(remove_spaces(plaintext))
    chunked_text = chunk_plaintext(remove_spaces(plaintext), len(key)-1)
    cipher_text = ''
    for chunk in chunked_text:
        cipher_text += apply_key(chunk, key)
        key = mutate_key(key)
    return reinsert_spaces(plaintext, cipher_text)


to_encrypt = """Our cryptosystem aims to minimize the risk of a security breach or leakage by
preventing an unauthorized agent from extracting important information quickly. The pattern is
difficult to detect, and is resistant to low-level frequency analysis attacks. Unless a more
sophisticated attack is employed, an unauthorized agent will not be able to break the cipher in
a short amount of time. Changing the key frequently will further ensure the confidentiality of
the encrypted data. Thus, we can confidently say that this achieves our goal for this
cryptosystem—to minimize the damage dealt to any agent at the event of a zero-day attack or
an unintentional leak of information. It is imperative to recognize the danger of putting the
safeguard of information solely on one system, so we strongly recommend the use of other
security measures in addition to our cryptosystem.
"""

key = 'jenkins'

print(encrypt(to_encrypt, key))

# list_key = list(zip([chr(i + ord('a')) for i in range(26)], range(26)))
# for pair in list_key:
#     print(pair)
