import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    #CSRF_ENABLED = True
    #SECRET = os.getenv('SECRET')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    TESTING = True
    SECRET_KEY = 'super_secret_xyzXYZ_xyzXYZ@xyzXYZ_123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/apptest?charset=utf8'
    JWT_BLACKLIST_TOKEN_CHECKS = 'all'

    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    # TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    # DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}