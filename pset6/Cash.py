import cs50

# get a positive change
while True:
    dollars = cs50.get_float("change: ")
    if (dollars > 0):
        break

cents = round(dollars * 100)
n = 0

while True:
    y = 0
    for y in range(cents // 25):
        cents = cents - 25
        n += 1
    x = 0
    for x in range(cents // 10):
        cents = cents - 10
        n += 1
    z = 0
    for z in range(cents // 5):
        cents = cents - 5
        n += 1
    for zz in range(cents // 1):
        cents = cents - 1
        n += 1
    if (cents == 0):
        break
print(n)

