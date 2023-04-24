from example.example import add, subtract, multiply, divide
import owntest


def test_add():
    assert add(2, 3) == 5
    assert add(2, 3, 5, 6, 8) == 24
    with owntest.raises(TypeError):
        multiply("a", 3)


def test_subtract():
    assert subtract(2, 3) == -1
    with owntest.raises(TypeError):
        multiply("a", 3)


def test_multiply():
    assert multiply(2, 3) == 6
    with owntest.raises(TypeError):
        multiply("a", 3)


def test_divide():
    assert divide(6, 3) == 2
    with owntest.raises(ZeroDivisionError):
        divide(6, 0)
    with owntest.raises(TypeError):
        multiply("a", 3)


@owntest.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 54)])
def test_eval(test_input, expected):
    print("====", test_input, expected)
    assert eval(test_input) == expected
