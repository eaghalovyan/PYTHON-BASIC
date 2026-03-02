import json
import os
import random
import re
import time
import uuid
import logging
import sys


class DataGenerator:
    def __init__(self, schema_input):
        self.schema = self._load_schema(schema_input)
        self._validate_schema_type()

    def _load_schema(self, schema_input):
        if os.path.exists(schema_input):
            try:
                with open(schema_input, "r") as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to read schema file: {e}")
                sys.exit(1)
        try:
            return json.loads(schema_input)
        except json.JSONDecodeError:
            logging.error(f"Data schema is neither a valid path nor valid JSON")
            sys.exit(1)

    def _validate_schema_type(self):
        valid_types = ['str', 'int', 'timestamp']
        for key, value in self.schema.items():
            if ":" not in value and not value.strip().startswith("["):
                logging.error(f"Schema error: Key '{key}' value must contain ':'")
                sys.exit(1)
            data_type = value.split(":")[0].strip() if ":" in value else "str"
            if data_type not in valid_types:
                logging.error(f"Schema error: Unsupported type '{data_type}' for key '{key}'")
                sys.exit(1)

    def parse_value(self, key, value_pattern):

        if ":" not in value_pattern:
            if value_pattern.strip().startswith("["):
                data_type = "str"  
                command = value_pattern.strip()
            else:
                return value_pattern
        else:
            parts = value_pattern.split(":", 1)
            data_type = parts[0].strip()

            command = parts[1].strip() if len(parts) > 1 else ""

        if data_type == "timestamp":
                if command:
                    logging.warning(f"Timestamp for '{key}' ignores values. '{command}' was provided.")
                return str(time.time())   
            
        if data_type == "str":
            if command == "rand":
                return str(uuid.uuid4())
                
            if command.startswith("[") and command.endswith("]"):
                try:
                    return random.choice(json.loads(command.replace("'", '"')))
                except:
                    pass
            return command if command else ""
            
        if data_type == "int":
            if not command:
                return None
                
            if command == "rand":
                return random.randint(0,10000)
                
            range_match = re.match(r"rand\((\d+), \s*(\d+)\)", command)
            if range_match:
                start, end = map(int, range_match.groups())
                return random.randint(start, end)
                

            if command.startswith("[") and command.endswith("]"):
                try:
                    return int(random.choice(json.loads(command)))
                except (ValueError, json.JSONDecodeError):
                    logging.error(f"Invalid list format for key '{key}': {command}")
                    sys.exit(1) 
                
            try:
                return int(command)
            except ValueError:
                logging.error(f"Value '{command}' for key '{key}' is not a valid integer.")
                sys.exit(1)

    def generate_line(self):
        return {k: self.parse_value(k,v) for k, v in self.schema.items()}




