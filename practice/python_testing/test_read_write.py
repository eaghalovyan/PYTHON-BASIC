"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import pytest
from python_part_2.task_read_write import combine_file_values

@pytest.fixture
def file_setup(tmp_path):
   input_dir = tmp_path/ "files" 
   input_dir.mkdir()
   result_file = tmp_path/"result.txt"
   return input_dir, result_file

def test_combine_file_values(file_setup):
    input_dir, result_file = file_setup

    (input_dir / "file_1.txt").write_text("10")
    (input_dir / "file_2.txt").write_text("")
    (input_dir / "file_3.txt").write_text("5")

    combine_file_values(input_dir, result_file)

    assert result_file.read_text() == "10, 5"


def test_empty_directory(file_setup):
    input_dir, result_file = file_setup

    combine_file_values(input_dir, result_file)

    assert result_file.read_text() == ""


def test_non_numeric_content(file_setup):
    input_dir, result_file = file_setup

    (input_dir / "file_1.txt").write_text("one")
    (input_dir / "file_2.txt").write_text("two")

    combine_file_values(input_dir, result_file)

    assert result_file.read_text() == "one, two"


def test_natural_sorting(file_setup):
    input_dir, result_file = file_setup

    (input_dir / "file_10.txt").write_text("10")
    (input_dir / "file_2.txt").write_text("2")

    combine_file_values(input_dir, result_file)

    assert result_file.read_text() == "2, 10"



