class Config():
    sql_uri = "postgresql://localhost/taxcli"


class TestingConfig(Config):
    sql_uri = "postgresql://localhost/taxcli-testing"

config = {
    'testing': TestingConfig,
    'default': Config
}
