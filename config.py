import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY='b_5#y2LF4Q8zxec]/'
    SESSION_COOKIE_SECURE = True

    # from Julian
    UPLOAD_EXTENSIONS = ['XLSX', 'XLS']
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]

class ProductionConfig(Config):
    
    UPLOAD_PATH   = "\\server\\uploads\\"
    DOWNLOAD_PATH = "\\server\\downloads\\"
    
class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False

    UPLOAD_PATH   = "C:\\Users\\user\\Documents\\Python_Scripts\\Phenome_tools\\server\\uploads\\"
    DOWNLOAD_PATH = "C:\\Users\\user\\Documents\\Python_Scripts\\Phenome_tools\\server\\downloads\\"

class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False