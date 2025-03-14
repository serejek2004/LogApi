class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://mac:1234@postgres_db:5432/FlaskLogApi'
    JWT_SECRET_KEY = 'secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'secret_key'
    TESTING = True
    DEBUG = True
