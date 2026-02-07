"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""
import pytest 
from python_part_2.task_exceptions import DivisionOnOneError, division

@pytest.mark.parametrize("x,y,expected", [
    (2, 2, 1),
    (10, 5, 2),
    (9, 3, 3),
    (7, 2, 3.5)
])
def test_division_ok(x,y,expected,capfd):
    result = division(x,y)
    captured = capfd.readouterr()
    assert result  == expected
    assert "Division finished" in captured.out

def test_division_by_zero(capfd):
    assert division(1,0) is None
    captured = capfd.readouterr() 
    assert "Division by 0" in captured.out
    assert "Division finished" in captured.out

def test_division_by_one(capfd):
    with pytest.raises(DivisionOnOneError, match="Division on 1 get the same result"):
        division(1,1)
    captured = capfd.readouterr() 
    assert "Division finished" in captured.out
