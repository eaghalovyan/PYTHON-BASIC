"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
import unittest
from unittest.mock import patch
from python_part_2.task_input_output import read_numbers

class TestReadNums(unittest.TestCase):

    def test_read_numbers_without_text_input(self):
        with patch("builtins.input", side_effect = ["1", "2", "3", "4"]):
            result = read_numbers(4)
        self.assertEqual(result, "Avg:2.50")


    def test_read_numbers_with_text_input(self):
        with patch("builtins.input", side_effect = ["1", "2", "hello", "pytest"]):
            result = read_numbers(4)
        self.assertEqual(result, "Avg:1.50")

    def test_no_numbers(self):
        with patch("builtins.input", side_effect = ["h", "g", "k", "m"]):
            result = read_numbers(4)
        self.assertEqual(result, "No numbers entered")


    if __name__ == "__main__":
        unittest.main()