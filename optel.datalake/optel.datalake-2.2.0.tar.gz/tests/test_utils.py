import pytest

import optel.datalake.utils as u


def write_small_file(p):
    p.write("test", mode="a")


def test_parallelize_pyspark_scheduling_valid_functions(tmpdir):
    p = tmpdir.mkdir("utils").join("test.txt")
    p.write("")
    functions = [write_small_file]*2
    u.parallelize_pyspark_scheduling(functions, arguments=(p,))

    assert p.read() == "testtest"


def test_parallelize_pyspark_scheduling_invalid_functions():
    functions = [lambda: 1/0]*2

    with pytest.raises(ZeroDivisionError):
        u.parallelize_pyspark_scheduling(functions)


def test_parallelize_pyspark_scheduling_mixed(tmpdir):
    functions = [lambda x: 1/0, write_small_file]

    p = tmpdir.mkdir("utils").join("test_mix.txt")
    p.write("")

    with pytest.raises(ZeroDivisionError):
        u.parallelize_pyspark_scheduling(functions, arguments=(p,))

    assert p.read() == "test"
