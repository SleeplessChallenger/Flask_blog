from flask import (Blueprint, render_template,
				   request, current_app)
from blog.models import Post
from flask_sqlalchemy import get_debug_queries
from blog.config import config

main = Blueprint('main', __name__)


'''The get_debug_queries() function returns the
queries issued during the request as a list
+ instead of warning we can opt for error'''
@main.after_app_request
def after_request(response):
	for query in get_debug_queries():
		if query.duration >= config.get('production').FLASKY_SLOW_DB_QUERY_TIME:
		# if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
			current_app.logger.warning(f'Slow query: {query.statement}, {query.parameters},\
													  {query.duration}, {query.context}')
	return response


@main.route('/')
@main.route('/home')
def home():
	# posts = Post.query.all()
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
																  per_page=5,
																  error_out=True)
	# aforewritten 'posts' will comprise how many posts per page, which page. 
	# By default there will be first page
	# It will be sent to home.html where rendering stuff will be done
	return render_template('home.html', posts=posts)

@main.route('/about')
def about():
	return render_template('about.html', title='About')
