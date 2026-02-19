"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""
import unittest
from unittest.mock import Mock, patch
from task_4 import print_name_address
import io
import json

class TestTask4(unittest.TestCase):

    @patch ('sys.stdout', new_callable = io.StringIO)
    def test_print_name_address_output(self, mock_stdout):
     
        mock_args = Mock()
        mock_args.number = 2
        mock_args.extra = ["--fake-address=address", "--some_name=name"]

        print_name_address(mock_args)

        raw_output = mock_stdout.getvalue()
        output = [line for line in raw_output.split('\n') if line.strip()]
        #output = mock_stdout.getvalue().strip().split('\n')

        print(f"\nDEBUG: Captured output list: {output}")
        self.assertEqual(len(output), 2, f"Should generate exactly 2 lines of output")
     
        for line in output:
            data = json.loads(line)
            self.assertIn("fake-address", data)
            self.assertIn("some_name", data)     
        

    @patch('sys.stdout', new_callable = io.StringIO)
    def test_invalid_provider(self, mock_stdout):
        mock_args = Mock()
        mock_args.number = 1
        mock_args.extra = [ "--invalid_field=not_a_real_provider"]

        print_name_address(mock_args)

        output = json.loads(mock_stdout.getvalue().strip())
        self.assertEqual(output["invalid_field"], "Error: Provider not found")


if __name__ == "__main__":
    unittest.main()