import sys

s = int(sys.argv[1])
x = 1
while s != 0:
    print(" " * (s - 1) + "#" * x)
    s -= 1
    x += 1
