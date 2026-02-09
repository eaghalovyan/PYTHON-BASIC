"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math

class OperationNotFoundException(Exception):
    pass

def math_calculate(function: str, *args):
        try:
            func = getattr(math, function)
        except AttributeError:
            raise OperationNotFoundException
        
        if len(args) > 2 or len(args) == 0:
             raise ValueError("Function must take 1 or 2 arguments")
        return func(*args)  
        
    


"""
Write tests for math_calculate function
"""
import pytest
@pytest.mark.parametrize(
    "function, args, expected",
    [
        ("log", (1024, 2), 10.0),   # 2 args
        ("ceil", (10.7,), 11),       # 1 arg
        ("sqrt", (16,), 4.0)         # 1 arg    
    ])
def test_math_calculate(function, args, expected):
     assert math_calculate(function, *args) == expected
     
@pytest.mark.parametrize(
    "function, args, expected",
     [
        ("hi", (16,), OperationNotFoundException),
        ("log", (), ValueError),
        ("log", (1,2,3), ValueError)
     ]
)
def test_math_calculate_exceptions(function, args, expected):
     with pytest.raises(expected):
          math_calculate(function, *args)