from flask import render_template, url_for, flash,\
				  redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.posts.forms import PostForm


posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, author=current_user, content=form.content.data)
		db.session.add(post)
		db.session.commit()
		flash('Now your post is published!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title='New Post',
							form=form, legend='New Post')

# home.html -> def post() -> post.html
@posts.route('/post/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
# {{ url_for('post', post_id=post.id) }}
# 1. home.html -> def post() -> post.html
# 2. if user's post -> Update & Delete buttons appear
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit() # commit new data from form without add() 
							# as data already in the db
		flash('You tweaked the post!', 'primary')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET': # if we just find ourselves on the page
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update post',
							legend='Update Post' ,form=form)

@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if current_user != post.author:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Now your post is erased!', 'primary')
	return redirect(url_for('main.home'))
