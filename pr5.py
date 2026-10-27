import random

# Генерируем множество из 6 случайных неповторяющихся чисел от 1 до 49
sportloto = set()

while len(sportloto) < 6:
  sportloto.add(random.randint(1, 49))

print("Выпавшие числа:", sportloto)
