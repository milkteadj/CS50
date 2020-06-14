# TODO

from cs50 import SQL
import sys
import csv

def main():

    if len(sys.argv) != 2:
        exit("Usage: import.py file")

    filename = sys.argv[1]

    if not (filename.endswith(".csv")):
        sys.exit("Must provide a *.csv")

    db = SQL("sqlite:///students.db")

    with open(filename, "r") as students:
        #csv.DictReader reads the first row as the keys for dict
        reader = csv.DictReader(students)

        for row in reader:
            #break name down to 2 or 3 parts lists
            break_name = row["name"].split(" ")

            #if student has no middle name:
            if len(break_name) == 2:
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                    break_name[0], None, break_name[1], row["house"], row["birth"])

            #if student has middle name:
            elif len(break_name) == 3:
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                    break_name[0], break_name[1], break_name[2], row["house"], row["birth"])

if __name__ == "__main__":
    main()