"""
Write function which reads a number from input nth times.
If an entered value isn't a number, ignore it.
After all inputs are entered, calculate an average entered number.
Return string with following format:
If average exists, return: "Avg: X", where X is avg value which rounded to 2 places after the decimal
If it doesn't exists, return: "No numbers entered"
Examples:
    user enters: 1, 2, hello, 2, world
    >>> read_numbers(5)
    Avg: 1.67
    ------------
    user enters: hello, world, foo, bar, baz
    >>> read_numbers(5)
    No numbers entered

"""


def read_numbers(n: int) -> str:
    total = 0
    num_count = 0
    for _ in range(n):
        num = input("enter number ")
        try:
            num = float(num)
            total += num
            num_count += 1
        except ValueError:
            pass
    if num_count > 0:
        return f"Avg:{total/num_count:.2f}"
    else: 
        return "No numbers entered"

# if __name__ == "__main__":
#     read_numbers(5)
