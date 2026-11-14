
import tkinter as tk


def calculate(operation):
    a = entry_a.get().strip()
    b = entry_b.get().strip()

    try:
        num_a = float(a)
        num_b = float(b)
    except ValueError:
        result_label.config(text="Ошибка ввода")
        return

    if operation == "+":
        result = num_a + num_b
    elif operation == "-":
        result = num_a - num_b
    elif operation == "*":
        result = num_a * num_b
    elif operation == ":":
        if num_b == 0:
            result_label.config(text="Деление на ноль")
            return
        result = num_a / num_b

    result_label.config(text=f"{result:.2f}")


# Создание главного окна
root = tk.Tk()
root.title("Калькулятор")
root.geometry("400x300")

# Поле для первого числа
tk.Label(root, text="Число A").grid(row=0, column=0, padx=10, pady=10)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1, padx=10, pady=10)

# Поле для второго числа
tk.Label(root, text="Число B").grid(row=1, column=0, padx=10, pady=10)
entry_b = tk.Entry(root)
entry_b.grid(row=1, column=1, padx=10, pady=10)

# Кнопки операций
tk.Button(root, text="+", width=5, command=lambda: calculate("+")).grid(row=2, column=0, padx=5, pady=15)
tk.Button(root, text="−", width=5, command=lambda: calculate("-")).grid(row=2, column=1, sticky="w", padx=5)
tk.Button(root, text="*", width=5, command=lambda: calculate("*")).grid(row=2, column=1, sticky="e", padx=5)
tk.Button(root, text=":", width=5, command=lambda: calculate(":")).grid(row=2, column=2, padx=5)

# Вывод результата
tk.Label(root, text="Результат:").grid(row=3, column=0, padx=10, pady=10)
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=1, padx=10, pady=10)

# Запуск приложения
root.mainloop()
