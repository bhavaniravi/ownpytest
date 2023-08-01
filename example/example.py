def test_type(func):
    """Tests that the type of the arguments are int."""

    def wrapper(*args, **kwargs):
        for arg in args:
            if not isinstance(arg, int):
                raise TypeError
        return func(*args, **kwargs)

    return wrapper


@test_type
def add(*args):
    return sum(args)


@test_type
def subtract(x, y):
    return x - y


@test_type
def multiply(x, y):
    return x * y


@test_type
def divide(x, y):
    return x / y
