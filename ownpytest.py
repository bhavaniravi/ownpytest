import os
import sys
import importlib
from inspect import getmembers, isfunction

fixtures_mapping = {}


def get_test_files():
    for dr in os.listdir(sys.path[0]):
        if dr != "tests":
            continue
        for files in os.listdir(dr):
            if not (files.startswith("test") and files.endswith(".py")):
                continue
            yield dr + "." + files[:-3]


def get_test_functions(file_path):
    module = importlib.import_module(file_path)
    for members in getmembers(module, isfunction):
        if "fixture_wrapper" in members[1].__name__:
            fixtures_mapping[members[0]] = members[1]
        elif members[0].startswith("test_"):
            yield members


def test_runner():
    errors = {}
    # get folder starts with tests in the current python path
    for dr in os.listdir(sys.path[0]):
        if dr != "tests":
            continue
        for files in get_test_files():
            for members in get_test_functions(files):
                test_function_name = members[0]
                test_function_object = members[1]
                # creating a mapping of fixtures as we find functions with fixture decorator

    if errors:
        print("\n------------------------ Errors -----------------------------------")
    else:
        print("\n------------- Success (No errors found) ---------------------------")


class raises:
    def __init__(self, exception):
        self.exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def parametrize(keys, values):
    # keys = "test_input,expected"
    # values = [("3+5", 8), ("2+4", 6), ("6*9", 54)]
    def decorator(func):
        params = []
        # params = [{"test_input": "3+5", "expected": 8}, {"test_input": "2+4", "expected": 6}, {"test_input": "6*9", "expected": 54}]

        # the function, to run subtests
        def wrapper(*args, **kwargs):
            """Runs the original test function with multiple params"""
            pass

        return wrapper

    return decorator


def fixture(function):
    def fixture_wrapper():
        # doesn't support yielding functions
        return function()

    return fixture_wrapper


if __name__ == "__main__":
    test_runner()
