import random

def process_matrix(matrix):
    if not matrix or not matrix[0]:
        return matrix

    m = len(matrix)
    n = len(matrix[0])

    # подсчет столбцов с отрицательными элементами
    negative_cols_count = 0
    for j in range(n):
        has_negative = False
        for i in range(m):
            if matrix[i][j] < 0:
                has_negative = True
                break
        if has_negative:
            negative_cols_count += 1

    # проверка условия
    if negative_cols_count < (n / 2):
        print(f"\nСтолбцов с отрицательными элементами: {negative_cols_count} из {n} (меньше половины).")
        print("Умножаем элементы нечетных столбцов  на 10.")
        for j in range(0, n, 2):
            for i in range(m):
                matrix[i][j] *= 10
    else:
        print(f"\nСтолбцов с отрицательными элементами: {negative_cols_count} из {n} (не меньше половины).")
        print("Возводим все отрицательные элементы в квадрат.")
        for i in range(m):
            for j in range(n):
                if matrix[i][j] < 0:
                    matrix[i][j] = matrix[i][j] ** 2

    return matrix


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{elem:6}" for elem in row))


def main():
    print("Доступные вычисления:")
    print("1 - Значения и размерность заданы в программе")
    print("2 - Ручной ввод размерности и элементов с клавиатуры")
    print("3 - Ввод размерности пользователем, заполнение случайными числами")

    try:
        mode = int(input("\nВыберите действие (1-3): "))
    except ValueError:
        print("Ошибка: введено не число.")
        return

    matrix = []

    if mode == 1:
        print("\n--- Режим 1: Матрица задана в программе ---")
        matrix = [
            [1, -2, 3, 4],
            [-3, 4, -2, 4],
            [9, 10, 11, 12]
        ]

    elif mode == 2:
        print("\n--- Режим 2: Ручной ввод ---")
        try:
            m = int(input("Введите количество строк (m): "))
            n = int(input("Введите количество столбцов (n): "))
            if m <= 0 or n <= 0:
                print("Размерность должна быть больше нуля.")
                return

            print("Введите элементы матрицы построчно (через пробел):")
            for i in range(m):
                row = list(map(int, input(f"Строка {i + 1}: ").split()))
                if len(row) != n:
                    print(f"Ошибка: ожидалось {n} элементов, введено {len(row)}.")
                    return
                matrix.append(row)
        except ValueError:
            print("Ошибка ввода. Ожидались целые числа.")
            return

    elif mode == 3:
        print("\n--- Режим 3: Случайная генерация ---")
        try:
            m = int(input("Введите количество строк (m): "))
            n = int(input("Введите количество столбцов (n): "))
            min_val = int(input("Введите нижнюю границу диапазона (например, -10): "))
            max_val = int(input("Введите верхнюю границу диапазона (например, 10): "))

            if m <= 0 or n <= 0:
                print("Размерность должна быть больше нуля.")
                return
            if min_val > max_val:
                print("Ошибка: нижняя граница не может быть больше верхней.")
                return

            for i in range(m):
                row = [random.randint(min_val, max_val) for _ in range(n)]
                matrix.append(row)
        except ValueError:
            print("Ошибка ввода. Ожидались целые числа.")
            return
    else:
        print("Некорректный режим работы.")
        return

    print("\nИсходная матрица:")
    print_matrix(matrix)

    # Обработка
    processed_matrix = process_matrix(matrix)

    print("\nРезультирующая матрица:")
    print_matrix(processed_matrix)

if __name__ == "__main__":
    main()