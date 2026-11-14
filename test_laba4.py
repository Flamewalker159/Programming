import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from laba4 import main, process_matrix, print_matrix

class TestProcessMatrix(unittest.TestCase):
    def process_without_messages(self, matrix):
        with redirect_stdout(StringIO()):
            return process_matrix(matrix)

    def test_less_than_half_multiplies_odd_columns(self):
        matrix = [[1, -2, 3, 4], [5, 6, 7, 8]]
        self.assertEqual(
            self.process_without_messages(matrix),
            [[10, -2, 30, 4], [50, 6, 70, 8]],
        )

    def test_half_or_more_squares_negative_values(self):
        matrix = [[-2, 1, 3, 4], [5, -6, 7, 8]]
        self.assertEqual(
            self.process_without_messages(matrix),
            [[4, 1, 3, 4], [5, 36, 7, 8]],
        )

    def test_odd_number_of_columns_and_no_negatives(self):
        matrix = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(
            self.process_without_messages(matrix),
            [[10, 2, 30], [40, 5, 60]],
        )

    def test_empty_matrix_is_returned_unchanged(self):
        for matrix in ([], [[], []]):
            with self.subTest(matrix=matrix):
                self.assertEqual(self.process_without_messages(matrix), matrix)


class TestProgramInput(unittest.TestCase):
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

    # позитивные сценарии

    def test_mode_1_builtin_matrix(self):
        output = self.run_program(["1"])
        self.assertIn("Режим 1", output)
        self.assertEqual(
            self.read_printed_matrix(output, "Результирующая матрица:", 3),
            [[1, 4, 3, 4], [9, 4, 4, 4], [9, 10, 11, 12]],
        )

    def test_mode_2_manual_input(self):
        output = self.run_program(["2", "2", "3", "1 2 3", "4 5 6"])
        self.assertIn("Режим 2", output)
        self.assertEqual(
            self.read_printed_matrix(output, "Результирующая матрица:", 2),
            [[10, 2, 30], [40, 5, 60]],
        )

    def test_mode_3_random_generation(self):
        with patch("laba4.random.randint", side_effect=[-2, 0, 3, -4]):
            output = self.run_program(["3", "2", "2", "-4", "3"])
        self.assertIn("Режим 3", output)
        self.assertEqual(
            self.read_printed_matrix(output, "Результирующая матрица:", 2),
            [[4, 0], [3, 16]],
        )

    # негативные сценарии

    def test_invalid_mode_selection(self):
        for value in ("abc", "", "1.5", "0", "4", "-1"):
            with self.subTest(value=value):
                output = self.run_program([value])
                self.assert_stops_before_processing(output)

    def test_mode_2_invalid_dimensions(self):
        for answers in (("2", "abc", "2"), ("2", "0", "2"), ("2", "2", "-1")):
            with self.subTest(answers=answers):
                output = self.run_program(list(answers))
                self.assert_stops_before_processing(output)

    def test_mode_2_invalid_matrix_row(self):
        output = self.run_program(["2", "1", "3", "1 x 3"])
        self.assertIn("Ошибка ввода", output)
        self.assert_stops_before_processing(output)

    def test_mode_3_invalid_range(self):
        output = self.run_program(["3", "2", "2", "10", "-10"])
        self.assertIn("нижняя граница не может быть больше верхней", output)
        self.assert_stops_before_processing(output)

if __name__ == "__main__":
    unittest.main(verbosity=2)