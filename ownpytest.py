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
                pass
    if errors:
        print("\n------------------------ Errors -----------------------------------")
    else:
        print("\n------------- Success (No errors found) ---------------------------")
    for member, ex in errors.items():
        pass


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
