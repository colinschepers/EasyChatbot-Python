class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}