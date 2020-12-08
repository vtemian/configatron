import tempfile

import pytest

from configatron import Configatron


@pytest.mark.parametrize(
    "fixture, expected",
    [
        (
            """
[ftp]   
port = 21
""",
            21,
        ),
        (
            """
[ftp]   
port = 21.1
""",
            21.1,
        ),
        (
            """
[ftp]   
port = -21
""",
            -21,
        ),
        (
            """
[ftp]   
port = -21.1
""",
            -21.1,
        ),
        (
            """
[ftp]   
port = 0
""",
            0,
        ),
        (
            """
[ftp]   
port = 1
""",
            1,
        ),
    ],
)
def test_parse_number(fixture, expected):
    with tempfile.NamedTemporaryFile(dir="/tmp") as tmpfile:
        tmpfile.write(fixture.encode())
        tmpfile.flush()

        config = Configatron(tmpfile.name)
        assert config.get("ftp").get("port") == expected


@pytest.mark.parametrize(
    "fixture, expected",
    [
        (
            """
[ftp]   
user = "www-data"
""",
            "www-data",
        ),
        (
            """
[ftp]   
user = "1"
""",
            "1",
        ),
        (
            """
[ftp]   
user = "no"
""",
            "no",
        ),
        (
            """
[ftp]   
user = "1.1"
""",
            "1.1",
        ),
        (
            """
[ftp]   
user = "-1"
""",
            "-1",
        ),
        (
            """
[ftp]   
user = "/a/b/c"
""",
            "/a/b/c",
        ),
    ],
)
def test_parse_string(fixture, expected):
    with tempfile.NamedTemporaryFile(dir="/tmp") as tmpfile:
        tmpfile.write(fixture.encode())
        tmpfile.flush()

        config = Configatron(tmpfile.name)
        assert config.get("ftp").get("user") == expected


@pytest.mark.parametrize(
    "fixture, expected",
    [
        (
            """
[ftp]   
path = /a/b/c
""",
            "/a/b/c",
        ),
        (
            """
[ftp]   
path = /
""",
            "/",
        ),
        (
            """
[ftp]   
path = /a
""",
            "/a",
        ),
        (
            """
[ftp]   
path = ///
""",
            "/",
        ),
    ],
)
def test_parse_path(fixture, expected):
    with tempfile.NamedTemporaryFile(dir="/tmp") as tmpfile:
        tmpfile.write(fixture.encode())
        tmpfile.flush()

        config = Configatron(tmpfile.name)
        assert config.get("ftp").get("path") == expected


@pytest.mark.parametrize(
    "fixture, expected",
    [
        (
            """
[ftp]   
config = a,b,c
""",
            ["a", "b", "c"],
        ),
        (
            """
[ftp]   
config = 1,2,3
""",
            ["1", "2", "3"],
        ),
        (
            """
[ftp]   
config = a,/,/
""",
            ["a", "/", "/"],
        ),
        (
            """
[ftp]   
config = no,yes,1,0
""",
            ["no", "yes", "1", "0"],
        ),
    ],
)
def test_parse_array(fixture, expected):
    with tempfile.NamedTemporaryFile(dir="/tmp") as tmpfile:
        tmpfile.write(fixture.encode())
        tmpfile.flush()

        config = Configatron(tmpfile.name)
        assert config.get("ftp").get("config") == expected


@pytest.mark.parametrize(
    "fixture, expected",
    [
        (
            """
[ftp]   
flag = no
""",
            False,
        ),
        (
            """
[ftp]   
flag = yes
""",
            True,
        ),
        (
            """
[ftp]   
flag = true
""",
            True,
        ),
        (
            """
[ftp]   
flag = false
""",
            False,
        ),
    ],
)
def test_parse_bool(fixture, expected):
    with tempfile.NamedTemporaryFile(dir="/tmp") as tmpfile:
        tmpfile.write(fixture.encode())
        tmpfile.flush()

        config = Configatron(tmpfile.name)
        assert config.get("ftp").get("flag") == expected
