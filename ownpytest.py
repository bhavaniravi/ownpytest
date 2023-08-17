import os
import sys
import importlib
from inspect import getmembers, isfunction
import traceback

fixtures_mapping = {}


def get_traceback(ex):
    tb = ex.__traceback__
    trace = []
    while tb is not None:
        if tb.tb_next is None:
            break
        tb = tb.tb_next

        trace.append(
            {
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno,
                "traceback": traceback.format_tb(tb),
                "message": ex.args,
            }
        )
    return trace


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
        if members[0].startswith("test_"):
            yield members


def test_runner():
    errors = {}
    # get folder starts with tests in the current python path
    for files in get_test_files():
        for test_function_name, test_function_object in get_test_functions(files):
            test_args = test_function_object.__code__.co_varnames
            # Run the tests here
            print("Running test: ", test_function_name)

    if errors:
        print("\n------------------------ Errors -----------------------------------")
        for test_name, err in errors.items():
            print(f"{test_name} failed with error: {get_traceback(err)}")
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

        # the function, to run subtests
        def wrapper(*args, **kwargs):
            pass

        return wrapper

    return decorator


def fixture(function):
    def fixture_wrapper():
        return function()

    return fixture_wrapper


if __name__ == "__main__":
    test_runner()
