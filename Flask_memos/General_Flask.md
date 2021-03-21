<h2> It is my memos from various resources that are related to general Flask</h2>

1. Want to run flask from terminal? And apply made changes automatically

export FLASK_APP = start.py
=> now we can run our file with: flask run

=> run it in 'debug mode': export FLASK_DEBUG=1

2. However, if you want to run it from CLI via `python3 some_app_name.py`:
`if __name__ == '__main__':
	app.run(debug=True)`

3. What is route?

	app.route is route for navigation: where we'll go entering /smth.
	If we want one function to handle multiple routes: add additional
	app.route to the same function

	The association between a URL and the function that handles it is called a route


	`@app.route('/') def index():
	return '<h1>Hello World!</h1>'`
==
	`def index():
		return '<h1>Hello World!</h1>'
		app.add_url_rule('/', 'index', index)`

Functions like `index()` that handle application URLs are called view functions

4. How to render templates with Jinja2?

use 'for' construction to render templates
`
	{% for post in posts %}
		<h1>{{ post.title }}</h1>
		<p>By {{ post.author }} on {{ post.date_posted }}</p>
		<p>{{ post.content }}</p>
	{% endfor %}
`
`
	use for/else to verify
	{ % if titel % }
		<title>FLask Blog - {{ title }}</title>
	{ % else % }
		<title>Flask blog</title>
	{ % endif % }
`
* title is passed into render_template(.., title='About')

5. It's good practice to have one file with similar code for many files
	and in detached files to have unqiue data only

	Use so-called inheritance. Child will overwrite `{% block content %}`

	a) `{% extends 'layout.html'}` # file with similar html
	b) `{% block content %}` # content is the name of block
	c) `{% endblock content %}`

6.	If you want to use .css file: 
	 `<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='main.css') }}">`

	'static' is folder and filename is obvious

7. To protect cookies you should use 'secret key':

	SECRET_KEY = os.environ.get('SECRET_KEY')
	Go to terminal and enter `python3`
	import secrets; secrets.token_hex(16) => `take the result`
	Then put it as environmental variable

	+ in pertinent .html file you should add:

	{{ form.hidden_tag() }}
	this will enable aforementioned 'secret key'

8. In url_for there are functions passed in which will navigate to pertinent routes 
	`<a class='ml-2' href="{{ url_for('login')}}"></a>`

9. `with` construction 

	with_categories=True allows to grab 'success', 'danger' etc
	flash(f'Account created for {form.username.data}!', 'success')
		  `
	      {% with messages = get_flashed_messages(with_categories=true) %}
          	{% if messages %}
          		{% for category, message in messages %}
          		 <div class='alert alert-{{ category }}'>
          		 	{{ message }}
          		 </div>
          		 {% endfor %}
          	{% endif %}
          {% endwith %}
          `
* Explanation: 
	1) get_flashed_messages will take messages that we sent to the template
	2) with_categories=true allow to grab 'success' category 
	3) if messages are returned
	4) because 'with_categories=true' we'll receive 2 values: category and message itself

10. Instead of '<a class="nav-item nav-link" href="/login">Login</a>' 
	it's better to use `{{ url_for('home')}}` as it's much more flexible

11. How to hash your password?

a)	`
	pip install flask-bcrypt
	from flask_bcrypt import Bcrypt
	bcrypt = Bcrypt()
	temp = bcrypt.generate_password_hash('test').decode('utf-8')
	bcrypt.check_password_hash(temp, 'somePass') => False
	bcrypt.check_password_hash(temp, 'test') => True
	`

b)	`
	from werkzeug.security import generate_password_hash, check_password_hash

	class User(db.Model): 
	# ...

	password_hash = db.Column(db.String(128))
	@property
	def password(self):
	raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
	self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
	return check_password_hash(self.password_hash, password)
	`

12. For anyone wondering how `validate_username()` and `validate_email()` are being called, these functions are called with the FlaskForm class that our RegistrationForm class inherited from. If you look at the definition for `validate_on_submit()`, and from there, the definition for validate(), that validate function contains the following line:

`inline = getattr(self.__class__, 'validate_%s' % name, None)`

There is a lot going on in the background, but from what I can tell, Flask is checking for extra functions created with the naming pattern: `validate_(field name)`, and later calling those extra functions.

13. add functionality to database models and it'll handle all the sessions in the 
	background for us 
	`@login_manager.user_loader` (user_loader is the main function). 
	This callback is used to reload the user object from the user ID stored in the session

14. `enctype="multipart/form-data"` : don't forget to add it while creating form for file attachment

15. `<img class='rounded-circle article-img' src="">` where rounded-circle is bootstrap
	and article-img is class in main.css

	`filename='profile_pics/' + post.author.image_file` : here also -> author is backref

16. `h2><a class="article-title" 
	 href="url_for('post', post_id=post.id)">{{ post.title }}</a></h2>`
	'post' is a function in the route.py

17. `<legend class='border-bottom mb-4'>{{ legend }}</legend>

	return render_template('create_post.html', title='New Post',
							form=form, legend='New Post')
	return render_template('create_post.html', title='Update Post',
							form=form, legend='Update Post')`

18. `{% for post in posts.items %}`  items were added after to iterate over 'post' object

	`for page in posts.iter_pages():
	print(page)` => number of pages will come out

	+ it can be customized => how many 1,2,None,4 will be

19. `{% for page_num in posts.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2) %}` : 
	
	first two show how many will be on the left and right edge, second two are how muany from current page

20. `{% if posts.page == page_num %}
            <a class='btn btn-info mb-4' href="{{ url_for('home',page=page_num) }}"> {{ page_num }} </a>
      {% else %}
           <a class='btn btn-outline-info mb-4' href="{{ url_for('home',page=page_num) }}"> {{ page_num }} </a>`

    btn without info means that current button will be dyed

21. 
	`posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) 
	order_by()` here allows to either new post be ahead or old ones


	Next:

	`for page in posts.iter_pages():
		print(page) `

		# there'll be 1 2 None 4 5 etc
		That None is like on real site when there're 
		many pages

	+ we can add parameters to `.iter_pages()` to customize it

22. `<a class='btn btn-info mb-4' href="{{ url_for('user_posts', username=user.username, page=page_num) }}"> {{ page_num }} </a>
      {% else %}
           <a class='btn btn-outline-info mb-4' href="{{ url_for('user_posts', username=user.username, page=page_num) }}"> {{ page_num }} </a>
      {% endif %}`

a) we changed for 'user_posts' otherwise if we click on the pagination => redirects for home page
b) added username = user.username for 'def user_posts()'

23. How to hash password?

	`from itsdangerous import TimedJSONWebSignatureSerializer as Serializer`
	`s = Serializer('secret', 30)` # secret key, expiration time in sec
	`token = s.dumps({'user_id': 1}).decode('utf-8')`
	`token` => some coded message
	`s.loads(token) => {'user_id': 1}` 

	!If we waited more than 30 sec -> error

24. Relative vs Absolute links

	`_external=True` makes absolute URL rather than relative. Because in 
	so-called external environment we need absolute whilst on the site/application
	relative will be ok

	Relative URLs are sufficient when generating links that connect the different routes of the application. Absolute URLs are necessary only for links that will be used outside of the web browser, such as when sending links by email.

25.	Application factory

	to tell Python that we want to have packages: create `__init__` in 
	those folders (even if `__init__` files don't consist of anything)

	we won't use 'app' in every file. Instead pertinent names. 
	Like 'users' in users -> `routes.py`

	+ in every `{url_for()}` there should be changed for the pertinent
	  route instead of function name of the route

26. After we've replaced 'app' in `config.py` and `init.py` 
	we need to substitute it for something. Flask has an 
	answer: `current_app`

27. How does Flask-Login works?

1. The user navigates to http://localhost:5000/auth/login by clicking on the “Log In” link. The handler for this URL returns the login form template.
2. The user enters their username and password, and presses the Submit button. The same handler is invoked again, but now as a POST request instead of GET.
a. The handler validates the credentials submitted with the form, and then invokes Flask-Login’s login_user() function to log the user in.
b. The login_user() function writes the ID of the user to the user session as a string.
c. The view function returns with a redirect to the home page.
3. The browser receives the redirect and requests the home page.
a. The view function for the home page is invoked, and it triggers the rendering of the main Jinja2 template.
b. During the rendering of the Jinja2 template, a reference to Flask-Login’s current_user appears for the first time.
c. The current_user context variable does not have a value assigned for this request yet, so it invokes Flask-Login’s internal function _get_user() to find out who the user is.
  User Authentication with Flask-Login | 113
d. The _get_user() function checks if there is a user ID stored in the user ses‐ sion. If there isn’t one, it returns an instance of Flask-Login’s AnonymousUser. If there is an ID, it invokes the function that the application registered with the user_loader decorator, with the ID as its argument.
e. The application’s user_loader handler reads the user from the database and returns it. Flask-Login assigns it to the current_user context variable for the current request.
f. The template receives the newly assigned value of current_user.

The login_required decorator builds on top of the current_user context variable by only allowing the decorated view function to run when the expression current_user.is_authenticated is True. The logout_user() function simply dele‐ tes the user ID from the user session.

28. How to enable Markdown in editing and viewing?

	1) in `__init__.py`: 
	`from flask_pagedown import PageDown`
	`pagedown = PageDown()
	pagedown.init_app(app)`

	2) in posts.forms
	`from flask_pagedown.fields import PageDownField
	content = PageDownField('You can write here', validators=[DataRequired()])`

	3)at the beginning after extends and content block in files that
	represent posts (or another html stuff)

	`{{ super() }}
	{{ pagedown.include_pagedown() }}`

	and in <div> where content is displayed:

    `{% if post.body_html %}
        {{ post.body_html | safe }}
    {% else %}
        {{ post.content }}
    {% endif %}`

    4) in `models.py`:
    	1) add field:
    		`body_html = db.Column(db.Text)`
    	2) after the fields:
    `@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
		'h1', 'h2', 'h3', 'p'] 
		target.body_html = bleach.linkify(bleach.clean(markdown(value, 
						   output_format='html'), tags=allowed_tags, strip=True))

	db.event.listen(Post.content, 'set', Post.on_changed_body)`
