import sys

a = int(sys.stdin.readline().replace(" ","")[2:])
sum = 0

for _ in range(a - 1):
    sum += int(sys.stdin.readline())

sys.stdout.write(str(sum))