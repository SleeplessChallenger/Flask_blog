# Flask_blog
This project is a blog with multiple features that is built with Flask.
Other technologies used in creation: HTML/CSS, Bootstrap, Jinja2, SQLAlchemy and a couple of others.

It encapsulates blog with ability to 
<ul>
<li>Register and login</li>
<li>Requirement to confirm account and feature of app to block users actions if so isn't done</li>
<li>Resending of emails feature</li>
<li>User's ability to alter their account and even pinpoint their location or erase their account</li>
<li>Weather feature to see it in various cities</li>
<li>Also it has migration which gives an option to save various version of your database</li>
<li>Users can write posts which can be written in raw MarkDown</li>
<li>Tried as well to create logging feature that will log slow queries</li>
<li>Et Cetera options</li>
</ul>

!!It is in development mode (with debug feature), hence don't use it in production
+ check below for issues that I couldn't resolve


<h2>Explanation:</h2>

You are welcome to use my project, but for smooth operation
you should bear in mind a couple of features:
	fine-tune 'environmental variables' otherwise you will
	see flow of errors. 
	Don't familiar with them? Check this video: <a href="https://youtu.be/5iWhQWVXosU">Click</a> 
	

	Which variables in particular? Well, you can look them in config.py
	+ I'll try to describe how to install them below.
	a) Secret key which will secure your cookies. How to use it?
		SECRET_KEY = os.environ.get('SECRET_KEY')
	Go to terminal and enter `python3`
	import secrets; secrets.token_hex(16) => `take the result`
	Then put it as environmental variable

	+ in pertinent .html file you should add:

	{{ form.hidden_tag() }}
	this will enable aforementioned 'secret key'

	b) Your database specification:
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	Example of my non-prodcution one:
		export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'

	c) MAIL_USERNAME = os.environ.get('DB_USER')
	   MAIL_PASSWORD = os.environ.get('DB_PASS')

	   for sending email


	d) Next step is installation of all required packages: 
	   install all from 'requirements.txt' to have all the required packages.

		<ol>
		How to do it? 
		<li>Open the terminal</li>
		<li>Run: pip install -r requirements.txt</li>
		</ol>


<h2>What does project do</h2>
My project follows <i>Application factory</i> structure

Superficially delineating the project:
1) `run.py` is the file which runs all the project
2) every folder has `__init__.py` to tell python that it's a package
3) `config.py` encapsulates all the environmental variables
4) `static & templates` are .html and .css files
5) `models.py` has my database models and relations
6) `main` folder has routes that handle start page
7) `users` is the most dense one which handles all the features pertinent to user (partially desribed in the beginning)
8) `posts` is the ones that enables creation of post/deletion/tweaking etc
9) `weather & calendar` are folders that enable ability to see weather and observe my Google calendar
10) `errors` is folder that will make custom errors instead of basic Flask ones
11) `api` is my ability to concoct API background, but stumbled upon a couple of issues


<h4> Salient note </h4> 
Here I'll make a refernce to brilliant resources that guided me

Flask:

1) https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
and his book 'Flask Web Development 2nd edition'

2) Corey Shafer's explanation of Flask: https://coreyms.com

3) Docs: 
	- flask: https://flask.palletsprojects.com/en/1.1.x/
	- flask-wtf: https://flask-wtf.readthedocs.io/en/stable/index.html
	- wtforms: https://wtforms.readthedocs.io/en/2.3.x/
	- flask-migrate: https://flask-migrate.readthedocs.io/en/latest/#
	- flask-login: https://flask-login.readthedocs.io/en/latest/

4) RealPython

5) Posts on StackOverflow:
	- https://stackoverflow.com/questions/19261833/what-is-an-endpoint-in-flask

6) SQLAlchemy:
	- explanation of `lazy` parameter: https://medium.com/@ns2586/sqlalchemys-relationship-and-lazy-parameter-4a553257d9ef

7) HTTP requests:
    MDN
	- MIME: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
	- Accept header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept

Bootstrap:
1) official docs: https://getbootstrap.com
2) some templates: https://bootsnipp.com

And of course: https://stackoverflow.com

<h3>Issues that I cannot solve</h3>
1. Although I implemented the feature where you can Follow/Unfollow another users and
   display hinges on `current_user` and `another user`. But didn't show in particular `followers/followed` as got trapped into `many-to-many` relationship issues.

   !! You can see my attempt to construct and fathom <i>many-to-many</i> in  `Flask memos` folder, `many-to-many` file.

2. I managed to create overall skeleton for the API, but `HTTPie` refused to test it and gave some hodgepodge barrage of errors

3. By and large, I tried to make linux server from scratch, there were errors that were above me to solve. I put some memos about it in `Flask memos`

4. In regard to hashing password I had 2 main options: Bcrypt and Werkzeug.
   The former was chosen as latter had some puzzles. Speaking about avatars: I used PIL, but Gravatar is lso an option

<h4>A little bit more about Flask migrate</h4>
Flask migrate is a little bit difficult to comprehend. Firstly, you can watch video of the creator:
<a href="https://youtu.be/IxCBjUapkWk">Click</a> 

	-If you still have question, then you can follow `Flask memos` folder and there find 
	 `Flask migrate` file to read

	-If you want some detailed explanation of the code points:
	 check files and navigate to those '#'

	-Also, I included various memos in the code itself. You can check them in the code.


Last note: below you can observe the tree (aka strucutre) of the project
tree of the project

```bash
.
├── Flask_memos
│   ├── Flask_Migrate.txt
│   ├── General_Flask.txt
│   ├── Linux\ server.txt
│   ├── Many_to_many.py
│   ├── REST_memos.txt
│   └── SQLAlchemy.txt
├── blog
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── authentication.py
│   │   ├── errors.py
│   │   ├── posts.py
│   │   └── users.py
│   ├── calendar
│   │   ├── __init__.py
│   │   └── calendar.py
│   ├── config.py
│   ├── errors
│   │   ├── __init__.py
│   │   └── handlers.py
│   ├── main
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── migrations
│   │   ├── README
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── d118c79ac758_.py
│   ├── models.py
│   ├── posts
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── site.db
│   ├── static
│   │   ├── main.css
│   │   ├── pics
│   │   │   ├── 1ba6eebe7b7eecf3.jpg
│   │   │   ├── 30a04d97b3524b66.jpg
│   │   │   ├── 42342f8b5d8c5ebf.JPG
│   │   │   ├── 9bc745e670b53437.JPG
│   │   │   ├── bd35e9dc8881abe1.JPG
│   │   │   ├── dbd3940de8cdfe30.jpg
│   │   │   └── default.JPG
│   │   └── register.css
│   ├── templates
│   │   ├── account.html
│   │   ├── all_users.html
│   │   ├── calendar.html
│   │   ├── conf.html
│   │   ├── create_post.html
│   │   ├── delete_account.html
│   │   ├── errors
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   ├── 500.html
│   │   │   └── invalid.html
│   │   ├── followers.html
│   │   ├── home.html
│   │   ├── layout.html
│   │   ├── login.html
│   │   ├── post.html
│   │   ├── register.html
│   │   ├── reset_request.html
│   │   ├── reset_token.html
│   │   ├── results.html
│   │   ├── user_info.html
│   │   ├── user_posts.html
│   │   └── weather.html
│   ├── test.db
│   ├── users
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── routes.py
│   │   └── utils.py
│   ├── validation_error.py
│   └── weather
│       ├── __init__.py
│       └── weather.py
├── requirements.txt
├── run.py
└── tests
    ├── __init__.py
    ├── test_Post_model.py
    ├── test_User_model.py
    ├── test_general.py
    └── test_routes.py
```
