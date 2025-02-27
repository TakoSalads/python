#08/19/24


def caeser_encryption(plaintext, shift):
    shift = shift % 26
    ciphertext = ""

    for char in plaintext:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            print(f"Encrypting: {char} with shift {shift} -> {shifted_char}")
            ciphertext += shifted_char
        else:
            ciphertext += char

    return ciphertext

def caeser_decryption(ciphertext, shift):
    shift = shift % 26
    return caeser_encryption(ciphertext, -shift)
