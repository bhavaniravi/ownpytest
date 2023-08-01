import os
import importlib
import traceback
from inspect import getmembers, isfunction, getsource
import sys
import ast

# from tests import test_python_basics

fixtures_mapping = {}


def count_yields_in_function(func):
    source = getsource(func)
    parsed_ast = ast.parse(source)

    def count_yields(node):
        if isinstance(node, ast.Yield):
            return 1
        count = 0
        for child_node in ast.iter_child_nodes(node):
            count += count_yields(child_node)
        return count

    return count_yields(parsed_ast)


def test_runner():
    errors = {}
    global fixtures_mapping
    # get folder starts with tests in the current python path
    for dr in os.listdir(sys.path[0]):
        if dr != "tests":
            continue
        for files in os.listdir(dr):
            if not (files.startswith("test") and files.endswith(".py")):
                continue
            # load the python module
            module = importlib.import_module(dr + "." + files[:-3])
            for members in getmembers(module, isfunction):
                # creating a mapping of fixtures as we find functions with fixture decorator
                if "fixture_wrapper" in members[1].__name__:
                    count_of_yield = count_yields_in_function(members[1].__wrapped__)
                    if count_of_yield > 1:
                        raise Exception(
                            f"Fixture member {members[0]} cannot yield more than once"
                        )
                    fixtures_mapping[members[0]] = members[1]

                elif members[0].startswith("test"):
                    print(
                        "Running test",
                        members[0],
                        # members[1],
                        # members[1].__code__.co_varnames,
                    )
                    func_args = []
                    for arg in members[1].__code__.co_varnames:
                        # if the argument is a fixture, call the fixture and persist the result
                        # if that in itself is a fixture, the we have a problem
                        if arg in fixtures_mapping:
                            fixture_return_value = fixtures_mapping[arg]()
                            # check if generator
                            if hasattr(fixture_return_value, "__next__"):
                                print("yielding generator")
                                func_args.append(next(fixture_return_value))
                                print("after yielding generator")
                            else:
                                func_args.append(fixture_return_value)
                    try:
                        members[1](*func_args)
                    except AssertionError as e:
                        errors[members[1]] = e
    if errors:
        print("\n------------------------ Errors -----------------------------------")
    else:
        print(
            "\n------------------------ Success (No errors found) -----------------------------------"
        )
    for member, ex in errors.items():
        # print(member.__name__)

        # tb = e.__traceback__
        # print(dir(tb.tb_frame.f_code.co_lnotab))
        # print(tb.tb_lineno, tb.tb_frame.f_code.co_filename)  # TypeError  # 2
        tb = ex.__traceback__
        while tb is not None:
            if tb.tb_next is None:
                break
            tb = tb.tb_next

        trace = []
        trace.append(
            {
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno,
                "traceback": traceback.format_tb(tb),
            }
        )
        print(type(ex).__name__, trace)


class raises:
    def __init__(self, exception):
        self.exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print("exit", exc_type, exc_val, exc_tb, self.exception)
        if exc_type != self.exception:
            raise AssertionError(f"expected={self.exception}, got={exc_type}")
        return True


def parametrize(keys, values):
    # keys = "test_input,expected"
    # values = [("3+5", 8), ("2+4", 6), ("6*9", 54)]
    def decorator(func):
        params = []
        # params = [{"test_input": "3+5", "expected": 8}, {"test_input": "2+4", "expected": 6}, {"test_input": "6*9", "expected": 54}]
        for value in values:
            param = {}
            for i, key in enumerate(keys.split(",")):
                param[key] = value[i]
            params.append(param)

        # the function, to run subtests
        def wrapper(*args, **kwargs):
            """Runs the original test function with multiple params"""
            for i, param in enumerate(params):
                print(f"Running subtest {func.__name__}", i + 1)
                func(**param)

        return wrapper

    return decorator


# all we do is mark it as fixture
def fixture(function):
    def fixture_wrapper():
        return function()

    return fixture_wrapper


if __name__ == "__main__":
    test_runner()
