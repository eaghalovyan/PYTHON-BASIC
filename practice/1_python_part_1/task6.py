"""
Write function which receives filename and reads file line by line and returns min and max integer from file.
Restriction: filename always valid, each line of file contains valid integer value
Examples:
    # file contains following lines:
        10
        -2
        0
        34
    >>> get_min_max('filename')
    (-2, 34)

Hint:
To read file line-by-line you can use this:
with open(filename) as opened_file:
    for line in opened_file:
        ...
"""
from typing import Tuple


def get_min_max(filename: str) -> Tuple[int, int]:
    ints = []
    with open('file.txt', 'r') as file:
        first = (int(file.readline().strip()))
        min = max = first

        for line in file:
            num = int(line.strip())
            if min > num:
                min = num
            if max < num:
                max = num
    file.close()
    return min,max

print(get_min_max('file.txt'))

