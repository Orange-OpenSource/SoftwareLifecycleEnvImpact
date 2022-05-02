"""Flask configuration"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_url = "sqlite:///" + os.path.join(basedir, "database.db")

SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = sqlite_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
