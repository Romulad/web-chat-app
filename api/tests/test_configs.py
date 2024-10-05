from ..app.configs import settings

def test_configs_attr():
    assert hasattr(settings, "mongodb_url")
    assert hasattr(settings, "mongodb_database")

def test_configs_type():
    assert isinstance(settings.mongodb_database, str)
    assert isinstance(settings.mongodb_url, str)

def test_configs_value():
    assert settings.mongodb_database == "chat_app"