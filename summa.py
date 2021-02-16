import sys

digit_string = sys.argv[1]
summa = 0
for i in digit_string:
    summa += int(i)
print(summa)
