import os
from random import randint
import csv
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import sys

sys.set_int_max_str_digits(100000)

FIB_DIR = './fib_results'
OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    return f1

def save_fib_to_file(i:int):
    file_path = os.path.join(FIB_DIR, f"{i}.txt")
    if not os.path.exists(file_path):
        fib_i = fib(i)   
        with open(file_path, "w", encoding = "utf-8") as f:
                f.write(f"{fib_i}") 
    return i   



def func1(array: list):
    if not os.path.exists(FIB_DIR):
        os.makedirs(FIB_DIR)

    unique_array = list(set(array))

    with ProcessPoolExecutor() as executor:
        executor.map(save_fib_to_file, unique_array)
        
        

def read_single_file(filename, folder_path):
    if filename.endswith(".txt"):         
        ordinal = filename.split(".")[0]
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                value = f.read().strip()
                return [int(ordinal), value]
        except Exception:
            return None
        
    return None





def func2(folder_path: str, result_file: str):
    data = []
    if not os.path.exists(folder_path):
        print("Source folder not found.")
        return
    
    all_files = os.listdir(folder_path)

    with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda f: read_single_file(f, folder_path), all_files))

    data = [r for r in results if r is not None]

    with open(result_file, "w", newline="", encoding="utf-8") as csv_result:
        writer = csv.writer(csv_result) 
        writer.writerow(["Ordinal", "Fibonacci_Value"])
        writer.writerows(data)   

    print(f"Successfully created {result_file}")


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    func1(array=[randint(1000, 100000) for _ in range(1000)])
    func2(folder_path="fib_results", result_file=RESULT_FILE)

    print(f"Success! Result saved to {RESULT_FILE}")