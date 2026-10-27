def series(x, eps):
    a = x / 6
    s = a
    n = 1

    while abs(a) > eps:
        n += 1
        a = a * (-x * (2 * n - 3)) / (
                (2 * n - 1) * 2 * n * (2 * n + 1)
        )
        s += a
    return s


A = float(input("Введите А: "))
B = float(input("Введите B: "))

if B <= A:
    print("некорреткное значение B, введите новое: ")
    B = float(input())

r = float(input("Введите шаг r: "))
if B - A < r:
    print("некорреткное значение шага, введите новое ")
    r = float(input())

eps = float(input("Введите точность eps: "))
if eps < 0 or eps > 1:
    print("некорреткное значение погрешности, введите новое ")
    eps = float(input())

print("============================")
print("|     X     |    f(x)  |")
print("============================")
while A <= B:
    y = series(A, eps)
    print(f"|    {A:8.5f}|   {y:10.5f}|")
    A += r
print("============================")
