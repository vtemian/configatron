import tempfile

import pytest

from configatron import Configatron


@pytest.mark.parametrize(
    "fixture, expected",
    [
        (
                """
    [ftp]   
    flag = yes
    flag<production> = no
    """,
                False,
        ),

        (
                """
    [ftp]   
    flag = yes
    flag<production> = yes
    flag<staging> = no
    """,
                False,
        ),

        (
                """
    [ftp]   
    flag = yes
    flag<development> = no
    flag<testing> = no
    """,
                True,
        ),
    ],
)
def test_overrides(fixture, expected):
    with tempfile.NamedTemporaryFile(dir="/tmp") as tmpfile:
        tmpfile.write(fixture.encode())
        tmpfile.flush()

        config = Configatron(tmpfile.name, ["production", "staging"])
        assert config.get("ftp").get("flag") == expected
