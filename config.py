class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY='b_5#y2LF4Q8zxec]/'
    SESSION_COOKIE_SECURE = True
    
    UPLOAD_EXTENSIONS = ['XLSX', 'XLS', 'CSV']
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]
    UPLOAD_PATH   = "uploads/"
    DOWNLOAD_PATH = "downloads/"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    
class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False