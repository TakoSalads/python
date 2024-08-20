#08/19/24

def ceasar_crack(ciphertext):
    for shift in range(1, 26):
        decrypted_text = ""
        for char in ciphertext:
            if char.isalpha():
                start = ord('A') if char.isupper() else ord('a')
                shifted_char = chr((ord(char) - start- shift) % 26 + start)
                decrypted_text += shifted_char
            else:
                decrypted_text += char
        print(f"Shift {shift}: {decrypted_text}")

ciphertext = input("Enter the Ceaser cipher to crack: ")
ceasar_crack(ciphertext)