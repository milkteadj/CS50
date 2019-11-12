from cs50 import get_string
from sys import argv

def main():
    # TODO
    if len(argv) != 2:
        print("Usage: python blee.py dictionary")
        exit(1)

    #open and read from the file and store in a python data structure
    file = open(argv[1], "r")
    #make a set of banned words
    bannedSet = set()
    for line in file:
        bannedSet.add(line.strip().lower())

    #prompts for a message
    plaintext = get_string("What message would you like to censor?\n")
    outputPT = ""
    words = plaintext.split()

    #check if each word in words, when lowered, is in the banned set.
    #if it is, add * of the same length. If it's not, add the og word.
    for word in words:
        if word.lower() in bannedSet:
            outputPT = outputPT + "*" * len(word) + " "
        else:
            outputPT += word + " "
    print(outputPT)

if __name__ == "__main__":
    main()
