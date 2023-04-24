import os
import importlib
from inspect import getmembers, isfunction

# from tests import test_python_basics


def test_runner():
    # get folder starts with tests in the current python path
    for dr in os.listdir("."):
        if dr.startswith("tests"):
            for files in os.listdir(dr):
                if files.startswith("test") and files.endswith(".py"):
                    # load the python module
                    module = importlib.import_module(dr + "." + files[:-3])
                    for members in getmembers(module, isfunction):
                        if members[0].startswith("test"):
                            print("Running test", members[0], members[1])
                            members[1]()

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


if __name__ == "__main__":
    test_runner()
