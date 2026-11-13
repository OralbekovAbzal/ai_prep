import csv
import random
import tracemalloc

tracemalloc.start()

with open("tx.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    tx = ["card", 0, "city"]
    for _ in range(10000000):
        tx[0] = f"…{random.randint(1000, 9999)}"
        tx[1] = random.randint(100, 100000)
        tx[2] = random.choice(["Astana", "Oskemen", "Almaty", "Semey", "Pavlodar"])
        writer.writerow(tx)

print(tracemalloc.get_traced_memory())