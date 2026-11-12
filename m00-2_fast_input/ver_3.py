import sys

f = sys.stdin.read().split("\n")

a = int(f[0].replace(" ", "")[2:])
sum = 0

for n in f[1:]:
    sum += int(n)

sys.stdout.write(str(sum))