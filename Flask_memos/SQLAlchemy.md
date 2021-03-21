<h2> It is my memos from various resources that are related to SQLAlchemy</h2>

1. SQLALchemy
`from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)`

CLI:
```bash
from start import db
db.create_all()
from start import User, Post
user_1 = User(username='Daniil', email='me@gmail.com', password='password')
db.session.add(user_1)
user_2 = User(username='Tony', email='gr@gmail.com', password='password')
db.session.add(user_2)
db.session.commit()
User.query.all()
User.query.first()
User.query.filter_by(username='Daniil').all() / User.query.filter_by(username='Daniil').first()
User.query.get(1) # get user by id + many of the commands above can be attached to variables
user_1.id / user_2.id
`

# Creating posts
`
post_1 = Post(title='Blog1', content='First post', user_id=user_1.id)
post_2 = Post(title='Blog2', content='Second post', user_id=user_1.id)
>>> db.session.add(post_1)
>>> db.session.add(post_2)
>>> db.session.commit()
`

=> posts = `db.relationship('Post', backref='author', lazy=True)` connects User class
	to Post class. `user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)`
	And here 'user.id' is table and column hence with small letter
`
post = Post.query.first()
post.user_id
# next we'll see how backref helps us:
post.author => User('Daniil', 'cd@gmail.com', 'default.jpg')

db.drop_all()
```

2. due to `backref='author'` we can use: `post.author.username` (home.html)

3. to see attributes of the post: 
	`from structure.models import Post
	posts = Post.query.paginate()`
	`dir(posts)` => will give many variables
	`posts.per_page` => how many per page
	`for x in posts.items:
		print(x)` => content of the post

`posts = Post.query.paginate(per_page=5) / = Post.query.paginate(per_page=5, page=2)`

4. to create environmental variables:

	1) in home directory type: `nano .bash_profile`
	2)`export DB_USER='EMAIL_USER'`
	  `export DB_PASS='EMAIL_PASS'`
	3) to access:
	   `os.environ.get('DB_USER')`
	   `os.environ.get('DB_PASS')`

5. `app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False` to speed up

6. `__tablename__ = 'roles'` to be used as Flask-SQLAlchemy does't name them in plural

7. Concise way: 
	`db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan, user_david])`

	 A database session can also be rolled back. If `db.session.rollback()` is called, any objects that were added to the database session are restored to the state they have in the data‐ base.

8. `str(User.query.filter_by(role=user_role))
	'SELECT users.id AS users_id, users.username AS users_username, users.role_id AS users_role_id \nFROM users \nWHERE :param_1 = users.role_id'`

9.	`@app.shell_context_processor
	def make_shell_context():
		return dict(db=db, User=User, Role=Role)`

The `app.shell_context_processor` decorator registers the function as a shell context function. When the flask shell command runs, it will invoke this function and register the items returned by it in the shell session. The reason the function returns a dictionary and not a list is that for each item you have to also provide a name under which it will be referenced in the shell, which is given by the dictionary keys.
