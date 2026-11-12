a = int(input().replace(" ", "")[2:])

sum = 0

for _ in range(a - 1):
    sum += int(input())

print(sum)