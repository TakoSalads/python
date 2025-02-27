#Kyle Button 
#08/19/24
#Purpose: To create a GUI program that allows the user
#to enter a message to be encrypted an produce the results on screen

#imports
import tkinter as tk
from tkinter import messagebox

def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            encrypted_text += shifted_char
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def encrypt_action():
    plaintext = plaintext_entry.get()
    try:
        shift = int(shift_entry.get())
        encrypted_text = caesar_encrypt(plaintext, shift)
        result_text.set(encrypted_text)
    except ValueError:
        messagebox.showerror("Invalid input", "Shift value must be an integer")

def decrypt_action():
    ciphertext = plaintext_entry.get()
    try:
        shift = int(shift_entry.get())
        decrypted_text = caesar_decrypt(ciphertext, shift)
        result_text.set(decrypted_text)
    except ValueError:
        messagebox.showerror("Invalid input", "Shift value must be an integer")

# Set up the main application window
root = tk.Tk()
root.title("Caesar Cipher")

# Create and place widgets
tk.Label(root, text="Text:").grid(row=0, column=0, padx=10, pady=10)
plaintext_entry = tk.Entry(root, width=50)
plaintext_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Shift:").grid(row=1, column=0, padx=10, pady=10)
shift_entry = tk.Entry(root, width=50)
shift_entry.grid(row=1, column=1, padx=10, pady=10)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_action)
encrypt_button.grid(row=2, column=0, padx=10, pady=10)

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_action)
decrypt_button.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Result:").grid(row=3, column=0, padx=10, pady=10)
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=400)
result_label.grid(row=3, column=1, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()