class Config(object):
    DEBUG = False
    TESTING = False

    SESSION_COOKIE_SECURE = True

    UPLOAD_EXTENSIONS = ['XLSX', 'XLS']
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]

    # UPLOAD_PATH = "C:\\Users\\user\\Documents"
    UPLOAD_PATH   = "C:\\Users\\user\\Documents\\Python_Scripts\\Phenome_tools\\server\\uploads\\"
    DOWNLOAD_PATH = "C:\\Users\\user\\Documents\\Python_Scripts\\Phenome_tools\\server\\downloads\\"

class ProductionConfig(Config):
    
    UPLOAD_PATH   = "\\server\\uploads\\"
    DOWNLOAD_PATH = "\\server\\downloads\\"
    
class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False