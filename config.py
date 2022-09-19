from flask_mysqldb import MySQL


class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'


class DevelopmentConfig(Config):
    DEBUG = True
    
    UPLOAD_FOLDER = './app/static/uploads'
    MAX_CONTENT_PATH = 16 * 1024 * 1024
    
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'idcschools'
    


config = {
    'configurations': DevelopmentConfig
}