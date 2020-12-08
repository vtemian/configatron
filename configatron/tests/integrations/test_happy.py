from configatron import Configatron


def test_simple():
    config = Configatron("configatron/tests/integrations/fixtures/simple.ini", ["production"])

    assert config.get("test").get("path") == "/a/b/c"
    assert config.get("test").get("number") == 123
    assert config.get("test").get("string") == "val"
    assert config.get("test").get("invalid") == {}
    assert config.get("test").get("over") == "production"

    assert config.get("test2").get("path") == "/a/b/c"
    assert config.get("test2").get("number") == 123
    assert config.get("test2").get("string") == "val"

    assert config.get("test3").get("simple") == ["a", "b", "c"]
    assert config.get("test3").get("bool") is False

    assert config.get("invalid") == {}
    assert config.get("invalid").get("invalid").get("another") == {}


def test_small_cache_size():
    config = Configatron("configatron/tests/integrations/fixtures/simple.ini", cache_options={"size": 1})

    assert config.get("test").get("over") == "blend"
    assert config.get("test").get("path") == "/a/b/c"
    assert config.get("test2").get("path") == "/a/b/c"
    assert config.get("test3").get("simple") == ["a", "b", "c"]
    assert config.get("test3").get("simple") == ["a", "b", "c"]


def test_small_cache_lifespan():
    config = Configatron("configatron/tests/integrations/fixtures/simple.ini", cache_options={"lifespan": 0})

    assert config.get("test").get("path") == "/a/b/c"
    assert config.get("test").get("path") == "/a/b/c"
    assert config.get("test").get("number") == 123
    assert config.get("test").get("string") == "val"
    assert config.get("test").get("invalid") == {}
