import caesarEncryption
import vigenereEncryption


def main():
    whichKind = input("Choose which kind of cipher: 1. Caesar, 2: Vigenère ")



    if whichKind == '1':
        phrase = input("Enter your phrase you'd like encrypted: ")
        encryptShift = int(input("Enter the shift value: "))

        encryption = caesarEncryption.caeser_encryption(phrase, encryptShift)
        print(f"Encrypted message: {encryption}")

        decryption = caesarEncryption.caeser_decryption(encryption, encryptShift)
        print(f"Decrypted message: {decryption}")



    elif whichKind == '2':
        phrase = input("Enter the phrase you'd like encrypted: ")
        keyword = input("Enter the keyword: ")

        encryption = vigenereEncryption.vigenere_encrypt(phrase, keyword)
        print(f"Encrypted Message: {encryption}")

        decryption = vigenereEncryption.vigenere_decrypt(encryption, keyword)
        print(f"Decrypted Message: {decryption}")



    else:
        print("Invalid Choice")

if __name__ == "__main__": 
    main()



