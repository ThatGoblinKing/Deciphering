import enchant
from threading import Thread
from string import ascii_lowercase, ascii_uppercase

MAX_THREADS = 5

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


def check_keys(min: int, max: int, correct_tally):
    for i in range(min, max):
        decrypted_string = caesar_decrypt(i, message)
        words = decrypted_string.split(" ")

        for word in words:
            # print(word, d.check(word))
            if d.check(word) is True:
                #print(f"Detected Word: {word}\nKey: {i}")
                correct_tally[i] += 1
            else:
                pass

correct_tally = {i:0 for i in range(26)}

message = input("Enter caesar obfuscated string: ")
threads = [None] * MAX_THREADS
for i in range(MAX_THREADS):
    min = int(i/MAX_THREADS)
    max = int((i + 1)/MAX_THREADS)
    threads[i] = Thread(target=check_keys, args=(min, max, correct_tally))
    threads[i].start()

for i in range(len(threads)):
    threads[i].join()



most_likely_key = max(d, key=lambda k: d[k])
print("Found key:", most_likely_key)
print("Decrypted Message:", caesar_decrypt(most_likely_key, message))
    
            # possible_decrypted.append([caesar_decrypt(i, z) for z in words])
    
# print(possible_decrypted)