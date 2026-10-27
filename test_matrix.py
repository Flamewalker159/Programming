import unittest
from contextlib import redirect_stdout
from io import StringIO

from laba4 import process_matrix


class TestProcessMatrix(unittest.TestCase):
    def process_without_messages(self, matrix):
        with redirect_stdout(StringIO()):
            return process_matrix(matrix)

    def test_less_than_half_multiplies_odd_columns(self):
        matrix = [
            [1, -2, 3, 4],
            [5, 6, 7, 8],
        ]
        result = self.process_without_messages(matrix)
        self.assertEqual(result, [
            [10, -2, 30, 4],
            [50, 6, 70, 8],
        ])

    def test_exactly_half_squares_negative_values(self):
        matrix = [
            [-2, 1, 3, 4],
            [5, -6, 7, 8],
        ]
        result = self.process_without_messages(matrix)
        self.assertEqual(result, [
            [4, 1, 3, 4],
            [5, 36, 7, 8],
        ])

    def test_more_than_half_squares_negative_values(self):
        matrix = [
            [-1, -2, 3, 4],
            [5, 6, -7, 8],
        ]
        result = self.process_without_messages(matrix)
        self.assertEqual(result, [
            [1, 4, 3, 4],
            [5, 6, 49, 8],
        ])

    def test_odd_number_of_columns(self):
        matrix = [
            [-2, 4, 5],
            [6, 7, 8],
        ]
        result = self.process_without_messages(matrix)
        self.assertEqual(result, [
            [-20, 4, 50],
            [60, 7, 80],
        ])

    def test_no_negative_columns(self):
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
        ]
        result = self.process_without_messages(matrix)
        self.assertEqual(result, [
            [10, 2, 30],
            [40, 5, 60],
        ])

    def test_empty_matrix_is_returned_unchanged(self):
        for matrix in ([], [[], []]):
            with self.subTest(matrix=matrix):
                result = self.process_without_messages(matrix)
                self.assertEqual(result, matrix)


if __name__ == "__main__":
    unittest.main(verbosity=2)
