import cs50

# get the height
while True:
    n = cs50.get_int("Height: ")
    if n >= 1 and n <= 8:
        break
# print the pyrimad
space = n - 1

for x in range(n):
    for y in range(space):
        print(" ", end="")

    for z in range(n - space):
        print("#", end="")
    space = space - 1
    print()
