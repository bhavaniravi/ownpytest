import pytest


def test_add():
    assert add(2, 3) == 5
    assert add(2, 3, 5, 6, 8) == 24
    with pytest.raises(TypeError):
        add("a", 3)


def test_subtract():
    assert subtract(2, 3) == -1
    with pytest.raises(TypeError):
        subtract("a", 3)


def test_multiply():
    assert multiply(2, 3) == 6
    with pytest.raises(TypeError):
        multiply("a", 3)


def test_divide():
    assert divide(6, 3) == 2
    with pytest.raises(ZeroDivisionError):
        divide(6, 0)

    with pytest.raises(TypeError):
        divide("a", 3)

@pytest.fixture
def conn_fixture():
    conn = sqlite3.connect("test.db")
    yield conn
    conn.close()
    yield conn


def test_conn(conn_fixture):
    with owntest.raises(sqlite3.OperationalError):
        assert conn_fixture.execute("SELECT * FROM test").fetchall() == [(1, "test")]