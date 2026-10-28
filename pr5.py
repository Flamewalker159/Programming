import random

sportloto = set()

while len(sportloto) < 6:
  sportloto.add(random.randint(1, 49))

print("Выпавшие числа:", sportloto)
