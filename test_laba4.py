import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import laba4
from laba4 import main, process_matrix, print_matrix

class TestProcessMatrix(unittest.TestCase):
    def process_without_messages(self, matrix):
        with redirect_stdout(StringIO()):
            return process_matrix(matrix)

    def test_less_than_half_multiplies_odd_columns(self):
        matrix = [[1, -2, 3, 4], [5, 6, 7, 8]]
        self.assertEqual(self.process_without_messages(matrix),
                         [[10, -2, 30, 4], [50, 6, 70, 8]])

    def test_exactly_half_squares_negative_values(self):
        matrix = [[-2, 1, 3, 4], [5, -6, 7, 8]]
        self.assertEqual(self.process_without_messages(matrix),
                         [[4, 1, 3, 4], [5, 36, 7, 8]])

    def test_more_than_half_squares_negative_values(self):
        matrix = [[-1, -2, 3, 4], [5, 6, -7, 8]]
        self.assertEqual(self.process_without_messages(matrix),
                         [[1, 4, 3, 4], [5, 6, 49, 8]])

    def test_odd_number_of_columns(self):
        matrix = [[-2, 4, 5], [6, 7, 8]]
        self.assertEqual(self.process_without_messages(matrix),
                         [[-20, 4, 50], [60, 7, 80]])

    def test_no_negative_elements(self):
        matrix = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(self.process_without_messages(matrix),
                         [[10, 2, 30], [40, 5, 60]])

    def test_empty_matrix_is_returned_unchanged(self):
        for matrix in ([], [[], []]):
            with self.subTest(matrix=matrix):
                self.assertEqual(self.process_without_messages(matrix), matrix)

    def test_single_column_with_negative_element_squares_it(self):
        matrix = [[-3], [2]]
        self.assertEqual(self.process_without_messages(matrix), [[9], [2]])


class TestProgramInput(unittest.TestCase):
    # проверка main

    def run_program(self, answers):
        output = StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            main()
        return output.getvalue()

    @staticmethod
    def read_printed_matrix(output, label, row_count):
        lines = output.splitlines()
        start = lines.index(label) + 1
        return [list(map(int, lines[start + i].split())) for i in range(row_count)]

    def assert_stops_before_processing(self, output):
        self.assertNotIn("Исходная матрица:", output)
        self.assertNotIn("Результирующая матрица:", output)

    def test_mode_1_builtin_matrix_full_program(self):
        output = self.run_program(["1"])
        self.assertIn("Режим 1", output)
        self.assertIn("Исходная матрица:", output)
        self.assertIn("Результирующая матрица:", output)
        self.assertIn("Возводим все отрицательные элементы в квадрат.", output)
        self.assertEqual(self.read_printed_matrix(output, "Результирующая матрица:", 3),
                         [[1, 4, 3, 4], [9, 4, 4, 4], [9, 10, 11, 12]])

    def test_mode_2_manual_input_full_program(self):
        output = self.run_program(["2", "2", "3", "1 2 3", "4 5 6"])
        self.assertIn("Режим 2", output)
        self.assertEqual(self.read_printed_matrix(output, "Исходная матрица:", 2),
                         [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(self.read_printed_matrix(output, "Результирующая матрица:", 2),
                         [[10, 2, 30], [40, 5, 60]])

    def test_mode_3_random_generation_full_program(self):
        with patch("laba4.random.randint", side_effect=[-2, 0, 3, -4]) as mocked_randint:
            output = self.run_program(["3", "2", "2", "-4", "3"])
        self.assertIn("Режим 3", output)
        self.assertEqual(mocked_randint.call_count, 4)
        self.assertEqual(self.read_printed_matrix(output, "Исходная матрица:", 2),
                         [[-2, 0], [3, -4]])
        self.assertEqual(self.read_printed_matrix(output, "Результирующая матрица:", 2),
                         [[4, 0], [3, 16]])

    def test_mode_3_equal_random_bounds_are_valid(self):
        with patch("laba4.random.randint", return_value=5):
            output = self.run_program(["3", "2", "2", "5", "5"])
        self.assertEqual(self.read_printed_matrix(output, "Исходная матрица:", 2),
                         [[5, 5], [5, 5]])
        self.assertEqual(self.read_printed_matrix(output, "Результирующая матрица:", 2),
                         [[50, 5], [50, 5]])

    def test_mode_letters_blank_and_decimal_are_rejected(self):
        for value in ("abc", "", "1.5"):
            with self.subTest(value=value):
                output = self.run_program([value])
                self.assertIn("Ошибка: введено не число.", output)
                self.assert_stops_before_processing(output)

    def test_unknown_numeric_modes_are_rejected(self):
        for value in ("0", "4", "-1", "99"):
            with self.subTest(value=value):
                output = self.run_program([value])
                self.assertIn("Некорректный режим работы.", output)
                self.assert_stops_before_processing(output)

    def test_mode_2_non_integer_dimensions_are_rejected(self):
        for answers in (("2", "abc", "2"), ("2", "2", "xyz")):
            with self.subTest(answers=answers):
                output = self.run_program(list(answers))
                self.assertIn("Ошибка ввода. Ожидались целые числа.", output)
                self.assert_stops_before_processing(output)

    def test_mode_2_zero_or_negative_dimensions_are_rejected(self):
        cases = (("0", "2"), ("-1", "2"), ("2", "0"), ("2", "-1"))
        for m, n in cases:
            with self.subTest(m=m, n=n):
                output = self.run_program(["2", m, n])
                self.assertIn("Размерность должна быть больше нуля.", output)
                self.assert_stops_before_processing(output)

    def test_mode_2_non_integer_matrix_element_is_rejected(self):
        output = self.run_program(["2", "1", "3", "1 x 3"])
        self.assertIn("Ошибка ввода. Ожидались целые числа.", output)
        self.assert_stops_before_processing(output)

    def test_mode_2_wrong_number_of_elements_is_rejected(self):
        cases = (("1 2", "2"), ("1 2 3 4", "4"))
        for row, actual_count in cases:
            with self.subTest(row=row):
                output = self.run_program(["2", "1", "3", row])
                self.assertIn(f"ожидалось 3 элементов, введено {actual_count}", output)
                self.assert_stops_before_processing(output)

    def test_mode_2_invalid_second_row_is_rejected(self):
        output = self.run_program(["2", "2", "2", "1 2", "3 q"])
        self.assertIn("Ошибка ввода. Ожидались целые числа.", output)
        self.assert_stops_before_processing(output)

    def test_mode_3_non_integer_dimensions_or_bounds_are_rejected(self):
        valid = ["3", "2", "2", "-5", "5"]
        for index in range(1, 5):
            answers = valid.copy()
            answers[index] = "abc"
            with self.subTest(invalid_field=index):
                output = self.run_program(answers)
                self.assertIn("Ошибка ввода. Ожидались целые числа.", output)
                self.assert_stops_before_processing(output)

    def test_mode_3_zero_or_negative_dimensions_are_rejected(self):
        cases = (("0", "2"), ("-1", "2"), ("2", "0"), ("2", "-1"))
        for m, n in cases:
            with self.subTest(m=m, n=n):
                output = self.run_program(["3", m, n, "-5", "5"])
                self.assertIn("Размерность должна быть больше нуля.", output)
                self.assert_stops_before_processing(output)

    def test_mode_3_reversed_random_range_is_rejected(self):
        output = self.run_program(["3", "2", "2", "10", "-10"])
        self.assertIn("нижняя граница не может быть больше верхней", output)
        self.assert_stops_before_processing(output)

    def test_print_matrix_outputs_rows(self):
        output = StringIO()
        with redirect_stdout(output):
            print_matrix([[1, -2], [30, 4]])
        self.assertEqual([list(map(int, row.split())) for row in output.getvalue().splitlines()],
                         [[1, -2], [30, 4]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
