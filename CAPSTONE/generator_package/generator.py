import argparse
import configparser
import json
import logging
import multiprocessing
import os
import sys
import random
import uuid
from generator_package.data_utils import DataGenerator

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def worker(args, file_path):
    gen = DataGenerator(args.data_schema)
    all_lines = []
    with open(file_path, 'w') as f:
        for _ in range(args.data_lines):
            all_lines.append(gen.generate_line)
            f.write(json.dumps(gen.generate_line()) + "\n")   

def clear_path(target_path, file_name_base):    
    for f in os.listdir(target_path):
        if f.startswith(file_name_base) and f.endswith(".json"):
            file_to_del = os.path.join(target_path, f)
            try:
                os.remove(file_to_del)
                logging.info(f"Deleted old file: {f}")
            except Exception as e:
                logging.warning(f"Could not delete {f}: {e}") 
                
def parse_args(defaults):
    parser = argparse.ArgumentParser(prog="magicgenerator", description = "Generate JSON test data.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument(
        "--path_to_save_files",
        default = defaults.get('path_to_save_files'),
        help = "Where to save test data"
        )
    parser.add_argument(
        "--files_count",
        type = int,
        default = defaults.getint('files_count'),
        help = "How many json files to generate"
        )
    parser.add_argument(
        "--file_name",
        default = defaults.get('file_name'),
        help = "Base file_name for generated files"
    )
    parser.add_argument(
        "--data_lines",
        type = int,
        default = defaults.getint('data_lines'),
        help = "Count of lines for each file"
    )
    parser.add_argument(
        "--file_prefix",
        choices = ['count', 'random', 'uuid'],
        default = defaults.get('file_prefix'),
        help = "Suffix for the filename if more than 1 file is generated."
    )
    parser.add_argument(
        "--data_schema",
        default = defaults.get('data_schema'),
        help = "Data schema for test data generation"
    )
    parser.add_argument(
        "--clear_path",
        action = "store_true",
        default = defaults.getboolean('clear_path'),
        help = "If enabled, deletes all existing files in the target directory that start with the base 'file_name' before generating new data."
)
    parser.add_argument(
        "--multiprocessing",
        type = int,
        default = defaults.getint('multiprocessing'),
        help = "The number of parallel processes to use for file generation."
    )
    
    return parser.parse_args()
    
def validate_path(path_input):
    abs_path = os.path.abspath(path_input)
    if os.path.exists(abs_path) and not os.path.isdir(abs_path):
        logging.error(f"Target path {abs_path} is not a directory.")
        sys.exit(1)
    os.makedirs(abs_path, exist_ok = True)
    return abs_path

def generate_file_list(abs_path, file_name, file_prefix, file_count):
    file_tasks = []
    for i in range(file_count):
            suffix = "" 
            if file_prefix == "count": suffix = f"_{i}"
            elif file_prefix == "random": suffix = f"_{random.randint(1,1000)}"
            elif file_prefix == "uuid": suffix = f"_{uuid.uuid4()}"
            file_tasks.append(str(os.path.join(abs_path, f"{file_name}{suffix}.jsonl")))
    return file_tasks


def main():
    setup_logging()
    logging.info("Program Started")

    config = configparser.ConfigParser()
    config.read("default.ini")
    defaults = config["DEFAULT"]

    args = parse_args(defaults)
    
    #Validate_Path
    abs_path = validate_path(args.path_to_save_files)

    #Clear_Path
    if args.clear_path:
        logging.info(f"Clearing files in {abs_path} matching {args.file_name}")
        clear_path(abs_path, args.file_name)
       

    
    logging.info("Starting Data Generation...")

    if args.files_count == 0:
        gen = DataGenerator(args.data_schema)
        for _ in range(args.data_lines):
            print(json.dumps(gen.generate_line()))
    else:
        file_tasks = generate_file_list(abs_path, args.file_name, args.file_prefix, args.files_count)
        
        if file_tasks:
            procs = min(args.multiprocessing, os.cpu_count())
            logging.info(f"Using {procs} processes to generate {len(file_tasks)} files.")
            
            with multiprocessing.Pool(procs) as pool:
                pool.starmap(worker, [(args, fp) for fp in file_tasks])

    logging.info("Data Generation Finished.")
    return 0

if __name__ == "__main__":
    main()