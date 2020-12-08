from unittest import mock

from configatron import Configatron


def test_get_from_lru():
    config = Configatron("/", validate=False)
    config.lru = {"test": "group"}

    assert config.get("test") == "group"
