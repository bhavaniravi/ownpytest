import os
import sys
import importlib
from inspect import getmembers, isfunction, isgeneratorfunction
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
        elif "fixture_wrapper" in members[1].__name__:
            fixtures_mapping[members[0]] = members[1]


def test_runner():
    errors = {}
    # get folder starts with tests in the current python path
    for dr in os.listdir(sys.path[0]):
        if dr != "tests":
            continue
        for files in get_test_files():
            for test_function_name, test_function_object in get_test_functions(files):

                test_args = test_function_object.__code__.co_varnames
                # Run the tests here
                print("Running test: ", test_function_name)
                test_args_to_pass = []
                generator_fixtures = []
                for arg in test_args:
                    if arg in fixtures_mapping:
                        fixture_function = fixtures_mapping[arg]
                        # check if generator
                        if isgeneratorfunction(fixture_function):
                            fixture_generator = fixture_function()
                            fixture_return_value = next(fixture_generator)
                            # Save for later so we can tear down
                            generator_fixtures.append(fixture_generator)
                        else:
                            fixture_return_value = fixture_function()
                        test_args_to_pass.append(fixture_return_value)
                    else:
                        test_args_to_pass.append(arg)
                try:
                    test_function_object(*test_args_to_pass)
                except AssertionError as err:
                    errors[test_function_name] = err
                finally:
                    # Tear down all the generator based fixtures
                    for fixture_return_value in generator_fixtures:
                        try:
                            next(fixture_return_value)
                        except StopIteration:
                            pass

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

        if exc_type is None:
            raise AssertionError(f"{self.exception} not raised")
        if exc_type is not self.exception:
            raise AssertionError(
                f"expected={self.exception} got \n {get_traceback(exc_val)}"
            ) from exc_val
        return True


def parametrize(keys, values):
    # keys = "test_input,expected"
    # values = [("3+5", 8), ("2+4", 6), ("6*9", 54)]
    def decorator(func):
        params = []
        # params = [{"test_input": "3+5", "expected": 8}, {"test_input": "2+4", "expected": 6}, {"test_input": "6*9", "expected": 54}]
        for value in values:
            params.append(dict(zip(keys.split(","), value)))
        # the function, to run subtests
        def wrapper(*args, **kwargs):
            """Runs the original test function with multiple params"""
            for i, param in enumerate(params):
                print(f"Running subtest {func.__name__}", i + 1)
                func(**param)

        return wrapper

    return decorator

def fixture(function):
    fixtures_mapping[function.__name__] = function

    return fixture

