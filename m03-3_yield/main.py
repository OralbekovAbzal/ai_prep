from collections import defaultdict
import tracemalloc

tracemalloc.start()
def read_rows(path):
    with open(path, mode="r") as f:
        for line in f:
            yield line.strip().split(",")

total = defaultdict(int)
for card, amount, city in read_rows("tx.csv"):
    total[card] += int(amount)

print(tracemalloc.get_traced_memory())