# User inputs
message = input("What do you wanna encrypt? ")
key = int(input("How many positions do you want to shift? "))

# Create empty string
encrypted = ""

# Loop through all the chars in the message
for i in message:
    # Shift character by shiftamount, then wrap using mod 26
    shifted = (ord(i) - ord("A") + key) % 26
    # Convert back to char and add to str
    encrypted += chr(shifted + ord('A'))

# Print the encrypted Message.
print(encrypted)