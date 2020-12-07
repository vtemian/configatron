from configurator.main import Configurator


def test_simple():
    config = Configurator("configurator/tests/integrations/fixtures/simple.ini")

    assert config.get("test").get("path") == "/a/b/c"
    assert config.get("test").get("number") == 123
    assert config.get("test").get("string") == "val"
