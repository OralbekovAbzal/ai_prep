import time
import sys

for i in range(5):
    print(i)
    time.sleep(1)

if int(sys.argv[1]) == 0:
    exit(0)
else:
    exit(1)