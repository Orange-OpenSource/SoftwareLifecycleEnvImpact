"""Flask configuration"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base Flask server config"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Production flask config"""

    FLASK_ENV = "production"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
    DEBUG = False


class DevelopmentConfig(Config):
    """Development flask config"""

    FLASK_ENV = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev.db")
    DEBUG = True


class TestConfig(Config):
    """Testing flask config"""

    FLASK_ENV = "testing"
    DEBUG = True
    TESTING = True
    DATABASE_URI = "sqlite:///:memory:"
    # SQLALCHEMY_ECHO = True
