
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 's00per s3cret s7ring'
    SESSION_TYPE = 'filesystem'
    MONGODB_SETTINGS = {
        'db': 'notebrain',
        'host': 'localhost',
        'port': 27017,
    }

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MAKO_TRANSLATE_EXCEPTIONS = False

class ProductionConfig(BaseConfig):
    pass
