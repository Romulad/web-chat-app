from ..app.configs import settings

def test_configs_attr():
    assert hasattr(settings, "mongodb_url")

def test_configs_type():
    assert isinstance(settings.mongodb_url, str)