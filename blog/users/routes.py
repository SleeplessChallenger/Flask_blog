from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                              RequestResetForm, ResetPasswordForm)
from blog.users.utils import save_pic, send_email, send_confirm_email

users = Blueprint('users', __name__)


'''Blueprint.before_request is called before each request within the blueprint.
If you want to call it before all blueprints, please use before_app_request.'''
@users.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed and request.endpoint \
	    and request.blueprint != 'users' and request.endpoint != 'static':
	    # if not confirmed then user can only visit 'users blueprint features'
			return redirect(url_for('users.first_confirm'))

@users.route('/confirm_first')
def first_confirm():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.home'))
	return render_template('conf.html')

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated: # .attribute comes from UserMixin class
		return redirect(url_for('main.home')) # so as logged user doesn't see those register&login
	form = RegistrationForm()
	if form.validate_on_submit(): # this func() triggers validate_funcs()
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		new_user = User(username=form.username.data, email=form.email.data,
						password=hashed_pass, country=form.country.data)
		db.session.add(new_user)
		db.session.commit()

		send_confirm_email(new_user)

		flash(f'Account for {form.username.data} \
				has been created. Verify your account by the link sent to the email', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Registration', form=form)

@users.route('/confirm/<token>')
@login_required
# user must be logged but unconfirmed
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.home'))
	if current_user.verify_token(token):
		db.session.commit()
		flash('You have successfully verified your account', 'success')
		return redirect(url_for('users.login'))
	flash('Issue: either link has expired or it is a wrong one')
	return redirect(url_for('users.register'))

@users.route('/confirm')
@login_required
def resend_conf():
	send_confirm_email(current_user)
	flash('A new message was sent to your mail')
	return redirect(url_for('users.login'))

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first() # check if user in db else None
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			# Once a user has authenticated, you log them in with the login_user function
			login_user(user, remember=form.check.data)
			next_page = request.args.get('next') # either route or None. Look below for expl
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
			# if initially accessed by '/account' => redirects to 'account.html'
			# elif firstly logged by button => redirects to 'home.html'
		flash('Something went wrong. Check your credetentials.', 'danger')
	return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
	logout_user()
	flash('You are now logged out')
	return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required 
# @.. enables that '/account' not being
# logged results in unathorized error
# But if we provide in __init__: ...view = 'func'
# that '.view' will redirect to it
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.pic.data:
			pic_file = save_pic(form.pic.data)
			current_user.image_file = pic_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.country = form.country.data
		db.session.commit()
		flash('Your acc now is altered!', 'warning')
		return redirect(url_for('users.account'))
	elif request.method == 'GET': # if we don't send data + if we simply open page
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.country.data = current_user.country
	image_file = url_for('static', filename='pics/' + current_user.image_file)
	return render_template('account.html', title='Account',
							form=form, image_file=image_file)

@users.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_account():
	if request.method == 'POST':
		user = User.query.filter_by(id=current_user.id).first()
		if not user:
			flash('No user with such id found', 'danger')
			return redirect(url_for('main.home'))
		elif current_user != user:
			flash('You cannot delete others account', 'danger')
			return redirect(url_for('main.home'))
		db.session.delete(user)
		db.session.commit()
		flash(f'{user.username} account has been erased!', 'info')
		return render_template('register.html')
	return render_template('delete_account.html')

@users.route('/follow/<string:username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		flash('No user with such username', 'danger')
		return redirect('main.home')
	if current_user.is_following(user):
		flash('You are already following this user','info')
		return redirect('main.home')
	current_user.follow(user)
	db.session.commit()
	flash(f'You now follow {username}', 'primary')
	return redirect(url_for('main.home'))

@users.route('/unfollow/<string:username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		flash('No user with such username', 'danger')
		return redirect('main.home')
	if not current_user.is_following(user):
		flash('You do not follow this user','info')
		return redirect('main.home')
	current_user.unfollow(user)
	db.session.commit()
	flash(f'You have unfollowed {username}', 'info')
	return redirect(url_for('main.home'))

@users.route('/followers/<string:username>')
def followers(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('No such user', 'danger')
		return redirect(url_for('users.all_users'))
	page = request.args.get('page', 1, type=int)
	page_2 = user.followers.paginate(page, per_page=5, error_out=False)

	# follows = [{'user': item.follower, 'timestamp': item.timestamp}
	# 		for item in page_2.items]

	return render_template('followers.html', user=user, title='Followers of', pagination=page_2)


	# return render_template('followers.html', user=user, title='Followed of',
	# 						pagination=page_2, follows=follows, endpoint='.followers')

@users.route('/followed_by/<string:username>')
def followed_by(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('No such user', 'danger')
		return redirect(url_for('users.all_users'))
	page = request.args.get('page', 1, type=int)
	page_2 = user.followed.paginate(page, per_page=5, error_out=False)



	return render_template('followers.html', user=user, title='Followed of', pagination=page_2)

@users.route('/all_users')
@login_required
def all_users():
	page = request.args.get('page', 1, type=int)
	users = User.query.paginate(per_page=5, page=page)
	return render_template('all_users.html', title='List of users', users=users)

# some temp route
@users.route('/all_user/username', methods=['GET', 'POST'])
@login_required
def user_info_2(username):
	user1 = User.query.filter_by(username=username).first()
	form = UpdateAccountForm()
	'''
	if current_user then it can see the form
	if not current_user then only observe
	+ after I've changed
	url_for('users.user_info', user=user.id) 
	rather than user=user aforewriiten stuff started working
	'''
	if form.validate_on_submit():
		if form.pic.data:
			pic_file = save_pic(form.pic.data)
			current_user.image_file = pic_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.country = form.country.data
		db.session.commit()
		flash('You has altered you account!', 'primary')
		return redirect(url_for('users.account'))
	elif request.method == 'GET': # if we don't send data + if we simply open page
		form.username.data = user1.username
		form.email.data = user1.email
		form.country.data = user1.country
	return render_template('user_info.html', title='User info',
							user=user1, form=form)



@users.route('/all_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_info(user_id):
	user1 = User.query.filter_by(id=user_id).first()
	form = UpdateAccountForm()
	'''
	if current_user then it can see the form
	if not current_user then only observe
	+ after I've changed
	url_for('users.user_info', user=user.id) 
	rather than user=user aforewriiten stuff started working
	'''
	if form.validate_on_submit():
		if form.pic.data:
			pic_file = save_pic(form.pic.data)
			current_user.image_file = pic_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.country = form.country.data
		db.session.commit()
		flash('You has altered you account!', 'primary')
		return redirect(url_for('users.account'))
	elif request.method == 'GET': # if we don't send data + if we simply open page
		form.username.data = user1.username
		form.email.data = user1.email
		form.country.data = user1.country
	return render_template('user_info.html', title='User info',
							user=user1, form=form)

@users.route('/user/<string:username>')
# 1. 'home.html' <a class="mr-2" href="{{ url_for('user_posts', username=posts.author.username) }}">
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user) \
			.order_by(Post.date_posted.desc())\
			.paginate(per_page=5, page=page)
	return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_email(user)
		flash('An email with further instructions has been sent to your email.', 'primary')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset password', form=form)

# we need to verify that the token from the email is active & valid
# we can get the token from the 'url'
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if not user:
		flash('Invalid or expired token', 'danger')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pass
		db.session.commit()
		flash('Your password has been updated! Be ready to log in', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset password',
							form=form)

