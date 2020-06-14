# TODO

import sys
from cs50 import SQL

def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: roster.py House")

    houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
    if (sys.argv[1] in houses) != True:
        sys.exit("Must select a Hogwarts House")

    db = SQL("sqlite:///students.db")

    #put students into a dictionary
    students = {}
    students = (db.execute("SELECT first, middle, last, birth FROM students WHERE house = :house ORDER BY last, first", house=sys.argv[1]))

    for student in students:
        first = student["first"]
        middle = student["middle"]
        last = student["last"]
        year = student["birth"]

        #if student does not have middle name
        if middle == None:
            print(f"{first} {last}, born {year}")

        #if they do have middle name:
        else:
            print(f"{first} {middle} {last}, born {year}")




if __name__ == "__main__":
    main()