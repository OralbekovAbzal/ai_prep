import sys

if len(sys.argv) < 2:
    print("Недостаточно параметров", file=sys.stderr)
    sys.exit(2)

count = 0
selected = 0
broken = 0

try:
    limit = int(sys.argv[1])
except ValueError:
    print("Неверный тип данных для параметра",file=sys.stderr)
    sys.exit(2)

for line in sys.stdin:
    count += 1
    clear_line = line.replace(" ", "")
    l = clear_line.split(",")
    if len(l) != 3:
        broken += 1
        continue
    try:
        amount = int(l[1])
        if amount < 0:
            broken += 1
            continue
        if amount > limit:
            sys.stdout.write(line)
            selected += 1
    except ValueError:
        broken += 1
        print(f"ValueError at row number {count}", file=sys.stderr)

print(f"Total: {count}, suspicious: {selected}, broken: {broken}",file=sys.stderr)