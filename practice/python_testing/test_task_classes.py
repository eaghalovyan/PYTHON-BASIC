"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

import pytest
import datetime
from datetime import timedelta
from python_part_2.task_classes import Teacher, Student, Homework

@pytest.fixture
def teacher():
    return Teacher("Dmitry", "Orlyakov")

@pytest.fixture
def student():
    return Student("Vladislav", "Popov")

def test_teacher_create_homework(teacher):
    hw = teacher.create_homework("New Task", 3)
    assert isinstance(hw, Homework)
    assert hw.text == "New Task"
    assert hw.num_of_days == 3
    assert isinstance(hw.created, datetime.datetime)
    assert hw.deadline == hw.created + timedelta(days=3)

def test_do_homework_active(teacher, student):
    hw = teacher.create_homework("Active task", 3)
    result = student.do_homework(hw)
    assert result == hw    

def test_do_homework_expired(teacher, student, capsys):
    hw = teacher.create_homework("Old Task", -1)
    result = student.do_homework(hw)
    captured = capsys.readouterr()
    assert result is None
    assert "You are late" in captured.out

def test_homework_is_active():
    hw = Homework("Active Task", 1)
    assert hw.is_active()
    hw.deadline = hw.created - timedelta(days=1)
    assert not hw.is_active()

def test_homework_negative_days():
    hw = Homework('Impossible task', -5)
    assert not hw.is_active()
    assert hw.deadline < hw.created

