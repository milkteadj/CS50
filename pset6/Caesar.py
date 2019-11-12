import cs50
import sys

#To get a key
if len(sys.argv) == 2:
    i = 0
    for i in range(len(sys.argv[1])):
        if sys.argv[1][i] < '0' or sys.argv[1][i] > '9':
            print("Usage: python caesar.py key")
            exit()
elif len(sys.argv) != 2:
    print("Command prompt: python caesar.py key\n")
    exit

#shift key into a number
key = int(sys.argv[1])

#print out text
plain = cs50.get_string("Plaintext:")
print("ciphertext: ", end="")

#
for j in range(len(plain)):
    if plain[j] >= 'a' and plain[j] <= 'z':
        newVal = chr((ord(plain[j]) + key - ord('a'))%26 + ord('a'))
        print(newVal, end="")
    elif plain[j] >= 'A' and plain [j] <= 'Z':
        newVal = chr((ord(plain[j]) + key - ord('A'))%26 + ord('A'))
        print(newVal, end="")
    else:
        print(plain[j], end="")
print()
