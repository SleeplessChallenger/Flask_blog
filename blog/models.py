from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from markdown import markdown 
import bleach
from blog.validation_error import ValidationError


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
'''
we place it here as we need to reload
user from the db

About db:

I opted for model which will help to build Many-to-Many
relationship instead of association table
as I have some additional features which makes
it difficult to work with simple table

Next, we have just users, no other tables. So,
self-referential relationships are used

Hence, we combine those 2 approaches in the class
'''

class Follow(db.Model):

	__tablename__ = 'follows'
	
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
							primary_key=True)

	followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
							primary_key=True)

	timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):

	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	image_file = db.Column(db.String(20), default='default.jpg', nullable=False)
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True,
							 cascade='all, delete-orphan')
	# lazy=True allows to retrieve all the posts made by the user in one go
	confirmed = db.Column(db.Boolean, default=False)
	country = db.Column(db.String(64))

	followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
								backref=db.backref('follower', lazy='joined'),
								lazy='dynamic', cascade='all, delete-orphan')

	followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
								 backref=db.backref('followed', lazy='joined'),
								 lazy='dynamic', cascade='all, delete-orphan')
	'''
	The default cascade options are appropriate for most situations,
	but there is one case in which the default cascade options do not
	work well for this many-to-many relationship. The default cascade
	behavior when an object is deleted is to set the foreign key in
	any related objects that link to it to a null value. But for
	an association table, the correct behavior is to delete the entries
	that point to a record that was deleted, as this effectively destroys the link.
	This is what the delete-orphan cascade option does.
	'''


	def get_reset_token(self, expires_sec=1800):
		temp = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return temp.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod # as we don't deal with instance of the user
	def verify_reset_token(token):
		temp = Serializer(current_app.config['SECRET_KEY'])
		try:
			this_user_id = temp.loads(token)['user_id'] 
			# 'user_id' is from get_reset_token's return statement
		except:
			return None
		return User.query.get(this_user_id)

	def generate_confirmation_token(self, expires_sec=1800):
		temp = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return temp.dumps({'confirm': self.id}).decode('utf-8')
	# this func() creates token and sets expiration to desired

	# def verify_auth_token(token):
	# 	temp = Serializer(current_app.config['SECRET_KEY'])
	# 	try:
	# 		data = temp.loads(token)
	# 	except:
	# 		return None
	# 	return User.query.get(data['id'])

	def verify_token(self, token):
		temp = Serializer(current_app.config['SECRET_KEY'])
		try:
			token_app = temp.loads(token.encode('utf-8'))
		except:
			return False
		if token_app.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)
		db.session.commit()


	def follow(self, user):
		if not self.is_following(user): # if user doesn't follow 'this' user
			relation = Follow(follower=self, followed=user)
			db.session.add(relation)

	def unfollow(self, user):
		relation = self.followed.filter_by(followed_id=user.id).first()
		if relation:
			db.session.delete(relation)

	def is_following(self, user):
		if user.id is None:
			return False
		return self.followed.filter_by(followed_id=user.id).first() is not None

	def is_followed_by(self, user):
		if user.id is None:
			return False
		return self.followers.filter_by(follower_id=user.id).first() is not None

	def to_json(self):
		json_user = {
					'url': url_for('blog.api.users.get_user', id=self.id),
					'username': self.username,
					'posts_url': url_for('blog.api.get_user_post', id=self.id)
					}
		return json_user

	def __repr__(self):
		return f"User: {self.username}, {self.email}, {self.image_file}"


class Post(db.Model, UserMixin):

	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	# we need to specify it. 'users.id': s here is due to __tablename__
	body_html = db.Column(db.Text)

	def __repr__(self):
		return f"Post: {self.title}, {self.date_posted}"

	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
		'h1', 'h2', 'h3', 'p'] 
		target.body_html = bleach.linkify(bleach.clean(markdown(value, 
						   output_format='html'), tags=allowed_tags, strip=True))

	def to_json(self):
		json_post = {
					'url': url_for('blog.api.get_post', id=self.id),
					'body': self.content,
					'body_html': self.body_html,
					'date_posted': self.date_posted,
					'author_url': url_for('blog.api.get_user', id=self.author)
					}

	@staticmethod
	def from_json(json_post):
		content_2 = json_post.get('body', None)
		if content_2 is None or content_2 == '':
			raise ValidationError('This post doesn not have a content')
		return Post(content=content_2)

db.event.listen(Post.content, 'set', Post.on_changed_body)
