import os

DEBUG=True
WTF_CSRF_CHECK_DEFAULT = False
SECRET_KEY = os.urandom(24)

DB_URL='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format('root','skx','127.0.0.1','3306','project_demo')
SQLALCHEMY_DATABASE_URI= DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS=False