"""
Write function which receives list of integers. Calculate power of each integer and
subtract difference between original previous value and it's power. For first value subtract nothing.
Restriction:
Examples:
    >>> calculate_power_with_difference([1, 2, 3])
    [1, 4, 7]  # because [1^2, 2^2 - (1^2 - 1), 3^2 - (2^2 - 2)]
"""
from typing import List


def calculate_power_with_difference(ints: List[int]) -> List[int]:
    if not ints:
        return []
    first = [ints[0] ** 2]
    for i in range(1,len(ints)):
        prev = ints[i-1]
        curr = ints[i]
        first.append(curr ** 2 - (prev ** 2 - prev))
    return first

print(calculate_power_with_difference([1, 2, 3]))
