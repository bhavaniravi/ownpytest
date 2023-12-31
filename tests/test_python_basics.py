import ownpytest as owntest
import sqlite3

from example.example import add, subtract, multiply, divide


def test_add():
    assert add(2, 3) == 5
    assert add(2, 3, 5, 6, 8) == 24


def test_subtract():
    assert subtract(2, 3) == -1


def test_multiply():
    assert multiply(2, 3) == 6


def test_divide():
    assert divide(6, 3) == 2


def test_raises():
    with owntest.raises(TypeError):
        add("a", 3)

    with owntest.raises(TypeError):
        divide("a", 3)

    with owntest.raises(ZeroDivisionError):
        divide(6, 0)

    with owntest.raises(TypeError):
        multiply("a", 3)

    with owntest.raises(TypeError):
        subtract("a", 3)


@owntest.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 54)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected


# @owntest.fixture
# def conn_fixture():
#     conn = sqlite3.connect("test.db")
#     yield conn
#     conn.close()


# def test_conn(conn_fixture):
#     with owntest.raises(sqlite3.OperationalError):
#         assert conn_fixture.execute("SELECT * FROM test").fetchall() == [(1, "test")]
