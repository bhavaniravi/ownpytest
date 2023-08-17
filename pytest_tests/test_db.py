import pytest
import sqlite3
import os


@pytest.fixture
def conn_fixture():
    conn = sqlite3.connect("test.db")
    conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER, name TEXT)")
    conn.execute("INSERT INTO test VALUES (1, 'test')")
    yield conn
    os.remove(f"{os.getcwd()}/test.db")

    conn.close()


@pytest.fixture
def cursor_fixture(conn_fixture):
    cur = conn_fixture.cursor()
    yield cur
    cur.close()


def test_select(cursor_fixture):
    cursor_fixture.execute("SELECT * FROM test")
    assert cursor_fixture.fetchall() == [(1, "test")]


def test_insert(cursor_fixture):
    cursor_fixture.execute("INSERT INTO test VALUES (2, 'test2')")
    cursor_fixture.execute("SELECT * FROM test")
    assert cursor_fixture.fetchall() == [(1, "test"), (2, "test2")]


def test_delete(cursor_fixture):
    cursor_fixture.execute("DELETE FROM test WHERE id = 2")
    cursor_fixture.execute("SELECT * FROM test")
    assert cursor_fixture.fetchall() == [(1, "test")]
