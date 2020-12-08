import tempfile

import pytest

from configatron import Configatron
from configatron.errors import ValidationError


@pytest.mark.parametrize("fixture, error", [
    ("""
[test
simple=1
""",
     "Invalid config: [test"),
    ("""
[
simple=1
""",
     "Invalid config: ["),
    ("""
[]
simple=1
""",
     "Invalid config: []"),
    ("""
]
simple=1
""",
     "Invalid config: ]"),
    ("""
name
simple=1
""",
     "Invalid config: name"),
    ("""
[⛔️]
simple=1
""",
     "Invalid config: [⛔️]"),
    ("""
[[double]]
simple=1
""",
     "Invalid config: [[double]]"),
    ("""
['double']
simple=1
""",
     "Invalid config: ['double']"),
    ("""
[+]
simple=1
""",
     "Invalid config: [+]"),
    ("""
[123]
[123]
""",
     "Duplicate group name: 123"),
])
def test_invalid_group_syntax(fixture, error):
    with tempfile.NamedTemporaryFile(dir='/tmp') as tmpfile:
        tmpfile.write(fixture.encode())
        tmpfile.flush()

        with pytest.raises(ValidationError) as excinfo:
            Configatron(tmpfile.name)

        assert error in str(excinfo.value)


@pytest.mark.parametrize("fixture, error", [
    ("""
    [group]
=
""",
    "Invalid property: ="),
    ("""
[group]
a!!!b
""",
     "Invalid config: a!!!b"),
    ("""
[group]
a=
""",
     "Invalid property: a="),
    ("""
[group]
a=
""",
     "Invalid property: a="),
    ("""
[group]
⛔️=
""",
     "Invalid property: ⛔️="),
    ("""
[group]
a=⛔️
""",
     "Invalid property: a=⛔️"),
    ("""
[group]
+=0
""",
     "Invalid property: +=0"),
    ("""
[group]
a :=0
""",
     "Invalid property: a :=0"),
    ("""
[group]
path = etc/app
""",
     "Invalid property: path = etc/app"),
    ("""
[group]
bool = yess
""",
     "Invalid property: bool = yess"),
    ("""
[group]
a = "single"
multiline
""",
     "Invalid config: multiline"),
    ("""
[group]
a = 'string'
""",
     "Invalid property: a = 'string'"),
    ("""
[group]
a = string
""",
     "Invalid property: a = string"),
    ("""
[group]
a = "quotes\""
""",
     "Invalid property: a = \"quotes\"\""),
])
def test_invalid_property_syntax(fixture, error):
    with tempfile.NamedTemporaryFile(dir='/tmp') as tmpfile:
        tmpfile.write(fixture.encode())
        tmpfile.flush()

        with pytest.raises(ValidationError) as excinfo:
            Configatron(tmpfile.name)

        assert error in str(excinfo.value)
