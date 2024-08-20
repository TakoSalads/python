#08/19/24

def vigenere_encrypt(plaintext, keyword):
    ciphertext = ""
    keyword = keyword.upper()
    keyword_length = len(keyword)
    keyword_index = 0
    
    for char in plaintext:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(keyword[keyword_index % keyword_length]) - ord('A')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            print(f"Encrypting: {char} with shift {shift} -> {shifted_char}")
            ciphertext += shifted_char
            keyword_index += 1
        else:
            ciphertext += char
    
    return ciphertext

def vigenere_decrypt(ciphertext, keyword):
    plaintext = ""
    keyword = keyword.upper()
    keyword_length = len(keyword)
    keyword_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(keyword[keyword_index % keyword_length]) - ord('A')
            shifted_char = chr((ord(char) - start - shift) % 26 + start)
            print(f"Decrypting: {char} with shift {-shift} -> {shifted_char}")
            plaintext += shifted_char
            keyword_index += 1
        else:
            plaintext += char
    
    return plaintext
