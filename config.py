import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/flask_medaipipe1")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
