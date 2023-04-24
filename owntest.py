import os
import importlib
from inspect import getmembers, isfunction

# from tests import test_python_basics

fixtures_mapping = {}


def test_runner():
    global fixtures_mapping
    # get folder starts with tests in the current python path
    for dr in os.listdir("."):
        if dr.startswith("tests"):
            for files in os.listdir(dr):
                if files.startswith("test") and files.endswith(".py"):
                    # load the python module
                    module = importlib.import_module(dr + "." + files[:-3])
                    for members in getmembers(module, isfunction):
                        if "fixture_wrapper" in members[1].__name__:
                            fixtures_mapping[members[0]] = members[1]
                        if members[0].startswith("test"):
                            print(
                                "Running test",
                                members[0],
                                members[1],
                                members[1].__code__.co_varnames,
                            )
                            func_args = []
                            print(fixtures_mapping)
                            for arg in members[1].__code__.co_varnames:
                                if arg in fixtures_mapping:
                                    func_args.append(
                                        fixtures_mapping[arg]()
                                    )  # fixture is a function to be called
                            members[1](*func_args)

            break


class raises:
    def __init__(self, exception):
        self.exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print("exit", exc_type, exc_val, exc_tb, self.exception)
        try:
            assert exc_type == self.exception
        except AssertionError:
            print(f"expected={self.exception}, got={exc_type}")
            return False
        return True


def parametrize(keys, values):
    def decorator(func):
        params = []

        for value in values:
            param = {}
            for i, key in enumerate(keys.split(",")):
                param[key] = value[i]
            params.append(param)

        def wrapper(*args, **kwargs):

            for i, param in enumerate(params):
                print("subtest running", i + 1)
                func(**param)

        return wrapper

    return decorator


def fixture(function):
    def fixture_wrapper():
        return function()

    fixtures_mapping[function.__name__] = function
    return fixture_wrapper


if __name__ == "__main__":
    test_runner()
