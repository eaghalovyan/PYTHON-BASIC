"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2021-10-05')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""
from datetime import datetime, date

class WrongFormatException(Exception):
    pass

def calculate_days(from_date: str) -> int:
    today = date.today()
    try:
        given_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        return (today - given_date).days
    except ValueError:
        raise WrongFormatException("Wrong date format")
       
# print(calculate_days("2026-12-05"))

"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""

import pytest
from freezegun import freeze_time

@freeze_time("2026-02-09")
def test_calculate_days():
    assert calculate_days("2026-02-05") == 4
    assert calculate_days("2026-02-10") == -1
    assert calculate_days("2026-02-09") == 0

@freeze_time("2026-02-09")
def test_wrong_format():
    with pytest.raises(WrongFormatException):
        calculate_days("2026/02/09")
    with pytest.raises(WrongFormatException):
        calculate_days("09-02-2026")
