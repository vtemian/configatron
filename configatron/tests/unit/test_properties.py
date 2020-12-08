import pytest

from configatron.nodes.property import string, number, path, boolean, array


@pytest.mark.parametrize("value, expected", [
    (1, None),
    (True, None),
    (False, None),
    ([1, 2, 3], None),
    ("a", None),
    ("/b/c/d", None),
    ("'a'", None),
    ('"a"', "a"),
    ('"yes"', "yes"),
    ('""', ""),
    ("", None),
])
def test_string(value, expected):
    assert string(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("1", 1),
    ("-1", -1),
    ("0", 0),
    ("1.1", 1.1),
    ("-1.1", -1.1),
    ("'-1.1", None),
    ("-1.10000", -1.1),
    ("-", None),
    (0, None),
    (1.1, None),
    (True, None),
    ([1, 2, 3], None),
])
def test_number(value, expected):
    assert number(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("/", "/"),
    ("//////", "/"),
    ("/a/a/", "/a/a"),
    ("/a/////a////", "/a/a"),
    ("'/a/a/'", None),
    ("/a/+/", "/a/+"),
    (0, None),
    (1.1, None),
    (True, None),
    ([1, 2, 3], None),
])
def test_path(value, expected):
    assert path(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("yes", True),
    ("1", True),
    ("true", True),
    ("no", False),
    ("0", False),
    ("false", False),
    ("", None),
    ("-1", None),
    ("-0", None),
    (0, None),
    (1.1, None),
    (True, None),
    ([1, 2, 3], None),
])
def test_boolean(value, expected):
    assert boolean(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("1,2,3", ["1", "2", "3"]),
    ("no,yes", ["no", "yes"]),
    ("[no,yes]", ["[no", "yes]"]),
    (",", ["", ""]),
    ("123", None),
    ("", None),
    (0, None),
    (1.1, None),
    (True, None),
    ([1, 2, 3], None),
])
def test_array(value, expected):
    assert array(value) == expected
