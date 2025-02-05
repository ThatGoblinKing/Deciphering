import enchant
from threading import Thread, Lock
from string import ascii_lowercase, ascii_uppercase
from datetime import datetime

FILE_PATH = 'decrypt.txt'
MAX_THREADS = 26
lock = Lock()

correct_tally = {i:0 for i in range(26)}
d = enchant.Dict("en_US")

def caesar_decrypt(key, encrypted_string):
    result = ""
    for char in encrypted_string:
        if char in ascii_uppercase:
            shifted = (ord(char) - ord("A") - key) % 26
            result += chr(shifted + ord("A"))
        elif char in ascii_lowercase:
            shifted = (ord(char) - ord("a") - key) % 26
            result += chr(shifted + ord("a"))
        else:
            result += char
    return result

def check_keys(min: int, max: int):
    global correct_tally
    for i in range(min, max):
        decrypted_string = caesar_decrypt(i, message)
        words = decrypted_string.split(" ")

        for word in words:
            # print(word, d.check(word))
            if d.check(word):
                #print(f"Detected Word: {word}\nKey: {i}")
                with lock:
                    correct_tally[i] += 1
            else:
                pass

step = 26 // MAX_THREADS
with open(FILE_PATH, 'r') as file:
    message = file.read()
threads = [None] * MAX_THREADS
startTime = datetime.now()
for i in range(MAX_THREADS):
    min = int(step * i)
    max_val = (i + 1) * step if i != MAX_THREADS - 1 else 26
    threads[i] = Thread(target=check_keys, args=(min, max_val))
    threads[i].start()

for i in range(len(threads)):
    threads[i].join()

time_taken = datetime.now() - startTime

most_likely_key = max(correct_tally, key=correct_tally.get)
print(f"""Found key: {most_likely_key}
Decrypted Message: {caesar_decrypt(most_likely_key, message)}
Time Taken: {time_taken.seconds}s {time_taken.microseconds / 1000}ms""")