"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

import os
from natsort import natsorted
folder = "./files"

def combine_file_values(input_folder, result_file = "result.txt"):
    values = []
    for filename in natsorted(os.listdir(input_folder)):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                content = f.read().strip()
                if content:
                    values.append(content)
        
    with open(result_file, "w") as f:
            f.write(", ".join(values))

combine_file_values(folder)
