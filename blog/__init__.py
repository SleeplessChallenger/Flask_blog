from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blog.config import config
from flask_migrate import Migrate
from flask_pagedown import PageDown


db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
# redirects to 'login' if '/account'
# typed unlogged (or the 'func' that
# you provide)
login_manager.login_message_category = 'info'
login_manager.login_message = 'Cannot access without being logged'

mail = Mail()
migrate = Migrate()
pagedown = PageDown()



def create_app(config_class=config['production']):
	app = Flask(__name__)
	app.config.from_object(config_class)
	# instead of app.config['MAIL_PORT'] etc stuff

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	migrate.init_app(app, db)
	pagedown.init_app(app)

	from blog.users.routes import users
	from blog.posts.routes import posts
	from blog.main.routes import main
	from blog.errors.handlers import errors
	from blog.weather.weather import weather
	from blog.calendar.calendar import calendar
	
	

	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)
	app.register_blueprint(weather)
	app.register_blueprint(calendar)

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api/v1')
	# we specify the version of the web service


	return app

'''
We initialized the creation of objects like db, bcrypt etc
outside of the function and without app inside so
that extension objects don't initially get bound
to the application. Using this design pattern, no 
application specific state is stored on the extension
object. So, one extension object can be used for multiple apps
'''
