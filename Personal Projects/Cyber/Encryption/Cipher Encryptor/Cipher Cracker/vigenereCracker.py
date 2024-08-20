from collections import Counter

def findKeyLength(ciphertext):
    for key_length in range(1, 21):
        chunks = [''.join(ciphertext[i::key_length]) for i in range(key_length)]
        coincidence_count = sum(sum(Counter(chunk).values()) for chunk in chunks)
        print(f"Key Length {key_length}: {coincidence_count} coincidences")

ciphertext = "RIJVSUYJN"
findKeyLength(ciphertext)