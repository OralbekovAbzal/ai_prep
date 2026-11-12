import sys
import random

sys.stdout.write("n = 10 000 000")

for _ in range(9_999_999):
    sys.stdout.write("\n")
    sys.stdout.write(str(random.randint(1, 1_000_000)))