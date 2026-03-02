import pytest
import json
import os
from CAPSTONE.generator_package.data_utils import DataGenerator
from CAPSTONE.generator_package.generator import clear_path, worker

@pytest.mark.parametrize("schema_val, expected_type", [
    ("int:10", int),
    ("str:hello", str),
    ("timestamp:", str)
])
def test_data_types(schema_val, expected_type):
    schema_json = json.dumps({"key": schema_val})
    gen = DataGenerator(schema_json)

    val = gen.generate_line()["key"]

    if expected_type is type(None):
        assert val is None
    else:
        assert isinstance(val, expected_type) 

@pytest.mark.parametrize("schema", [
    {"age": "int:rand(10, 20)"},
    {"status": "str:['active', 'idle']"},
    {"id": "str:rand"}
])
def test_schema(schema):
    gen = DataGenerator(json.dumps(schema))
    assert list(gen.generate_line().keys()) == list(schema.keys())

def test_schema_from_file(tmp_path):
    schema_file = tmp_path/"schema.json"
    schema_content = {"name": "str:rand"}
    schema_file.write_text(json.dumps(schema_content))

    gen = DataGenerator(str(schema_file))
    assert "name" in gen.generate_line()
    

def test_clear_path(tmp_path):
    old_file = tmp_path/ "test_data_old.json"
    old_file.write_text("old_data")

    clear_path(str(tmp_path), "test_data")
    assert not os.path.exists(old_file)


def test_file_saving(tmp_path):

    class MockArgs:
        data_schema = '{"id": "int:1"}'
        data_lines = 5

    target_file = tmp_path/ "output.json"
    worker(MockArgs(), str(target_file))

    assert target_file.exists()
    lines = target_file.read_text().strip().split('\n')
    assert len(lines) == 5
    assert json.loads(lines[0]) == {"id": 1}

def test_multiprocessing_file_count(tmp_path):

    file_name = "multi_test"
    file_count = 4
    
    file_tasks = [str(tmp_path/f"{file_name}_{i}.json") for i in range(file_count)]

    assert len(file_tasks) == 4
    assert file_tasks[0].endswith("multi_test_0.json")
    assert file_tasks[3].endswith("multi_test_3.json")

def test_multiprocessing():
    input_val = 1000
    cpu_limit = os.cpu_count()

    final_val = min(input_val, cpu_limit)

    assert final_val == cpu_limit
