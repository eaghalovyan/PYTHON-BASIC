"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import json
from faker import Faker

def print_name_address(args: argparse.Namespace) -> None:
    fake = Faker()
    fields = {}
    for item in args.extra:
        if item.startswith("-") and "=" in item:
            key, provider = item.lstrip("-").split("=", 1)
            fields[key] = provider

    for _ in range (args.number):
        output = {}
        for field_name, provider_name in fields.items():
            try:
                method = getattr(fake, provider_name)
                output[field_name] = method()
            except AttributeError:
                output[field_name] = f"Error: Provider not found"

        print(json.dumps(output))


if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Generate fake data dictionaries.")
        parser.add_argument("number", type = int, help = "Number of instance to generate")
        args, extra_args = parser.parse_known_args()

        args.extra = extra_args
        print_name_address(args)



