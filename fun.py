x = list(range(10))
import random

y = [random.randint(0,1) for i in range(10)]
print(y)
print(x)
np = y == 1
print(len(np))