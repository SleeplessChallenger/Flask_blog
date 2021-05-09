from flask import jsonify, request, g, url_for, current_app
from blog import db
from blog.models import Post
from . import api
from .errors import not_rights


@api.route('/posts/<int:id>')
def get_post(id):
	post = Post.query.get_or_404(id)
	return jsonify(post.to_json())

@api.route('/posts/')
def get_posts():
	page = request.args.get('page', 1, type=int)
	posts =  Post.query.paginate(page=page,
				     per_page=5,
				     error_out=False)
	prev = None
	if posts.has_prev:
		prev = url_for('blog.api.get_posts', id=id, page=page-1)
	next = None
	if posts.has_next:
		next = url_for('blog.api.get_posts', id=id, page=page+1)
	return jsonify({
			'posts': [x.to_json() for x in posts.items()],
			'prev': prev,
			'next': next,
			'count': posts.items().total
	})

@api.route('/posts/', methods=['POST'])
def new_post():
	post = Post.from_json(request.json)
	post.author = g.current_user
	db.session.add(post)
	db.session.commit()
	return jsonify(post.to_json()), 201,\
				   {'country': url_for('blog.api.get_post', id=post.id)}

@api.route('/posts/<int:id>', methods=['PUT'])
def edit_post(id):
	post = Post.query.get_or_404(id)
	if g.current_user != post.author:
		return not_rights('Only the author cn edit')
	post.content = request.json.get('content', post.content)
	db.session.add(post)
	db.session.commit()
	return jsonify(post.to_json())
