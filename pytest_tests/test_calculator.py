import pytest
from example.example import add, subtract, multiply, divide
import sqlite3
import os


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
    with pytest.raises(TypeError):
        add("a", 3)

    with pytest.raises(TypeError):
        divide("a", 3)

    with pytest.raises(ZeroDivisionError):
        divide(6, 0)

    with pytest.raises(TypeError):
        multiply("a", 3)

    with pytest.raises(TypeError):
        subtract("a", 3)


@pytest.fixture
def conn_fixture():
    conn = sqlite3.connect("test.db")
    yield conn
    conn.close()
    os.remove(f"{os.getcwd()}/test.db")


def test_conn(conn_fixture):
    with pytest.raises(sqlite3.OperationalError):
        conn_fixture.execute("SELECT * FROM test").fetchall() == [(1, "test")]
