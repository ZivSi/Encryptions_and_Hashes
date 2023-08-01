def encrypt(message, key="password"):
    encrypted = ""

    for index, letter in enumerate(message):
        key_index = index % len(key)

        encrypted += chr(ord(letter) ^ ord(key[key_index]))

    return encrypted


def decrypt(message, key="password"):
    return encrypt(message, key)
