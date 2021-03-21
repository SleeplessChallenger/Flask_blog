from flask import jsonify, request, current_app, url_for
from . import api
from blog.models import User, Post


@api.route('/users/<int:id>')
def get_user(id):
	user = User.query.get_or_404(id)
	return jsonify(user.to_json())

@api.route('/users/<int:id>/posts/')
def get_user_post(id):
	user = User.query.get_or_404(id)
	page = request.args.get('page', 1, type=int)
	posts = user.posts.order_by(Post.date_posted.desc()).paginate(page=page,
																  per_page=5,
																  error_out=False)
	prev = None
	if posts.has_prev:
		prev = url_for('blog.api.get_user_post', id=id, page=page-1)
	next = None
	if posts.has_next:
		next = url_for('blog.api.get_user_post', id=id, page=page+1)
	return jsonify({
					'posts': [x.to_json() for x in posts.items()],
					'prev': prev,
					'next': next,
					'count': posts.items().total
					})
