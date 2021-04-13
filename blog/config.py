import os


class Config:
	API_KEY = os.environ.get('API_KEY')
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('DB_USER')
	MAIL_PASSWORD = os.environ.get('DB_PASS')
	# below 2 rows are essential for enabling 
	# auery performance in the production
	SQLALCHEMY_RECORD_QUERIES = True
	FLASKY_SLOW_DB_QUERY_TIME = 0.5

	
class TestDB:
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_TEST_DB_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get('SECRET_KEY')


config = {
	'production': Config,
	'testDB': TestDB
}
