import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://user:password@hangman-database:5432/hangman"
    )


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://user:password@hangman-test-database:5432/test_db"
    )


# class DevelopmentConfig(Config):
#     SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost:5432/hangman"


# class TestingConfig(Config):
#     SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
