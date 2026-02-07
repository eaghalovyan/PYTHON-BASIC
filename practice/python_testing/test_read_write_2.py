"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
from python_part_2.task_read_write_2 import generate_words

def test_generate_words():
    words = generate_words(5)
    assert len(words) == 5
    for word in words:
        assert word.islower()
        assert word.isalpha()
        assert 3 <= len(word) <= 10

def test_file_writing(tmp_path):
    words = generate_words(3)
    file1 = tmp_path/"result2.txt"
    file2 = tmp_path/"result2_reversed.txt"

    file1.write_text("\n".join(words), encoding = "utf-8")
    file2.write_text(", ".join(reversed(words)), encoding = "cp1252")

    content1 = file1.read_text(encoding="utf-8")
    assert content1 == "\n".join(words)

    content2 = file2.read_text(encoding="cp1252")
    assert content2 == ", ".join(reversed(words))