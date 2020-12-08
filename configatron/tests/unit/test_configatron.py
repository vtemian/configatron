from unittest import mock

from configatron import Configatron


def test_get_from_lru():
    config = Configatron("/", validate=False)
    config.lru = {"test": "group"}

    assert config.get("test") == "group"


def test_get_from_index():
    config = Configatron("/", validate=False)

    group = mock.MagicMock()
    group.name = "test"
    group.is_fresh = True

    config.index = {"test": group}

    assert config.get("test") == group
    assert config.lru.get("test") == group
