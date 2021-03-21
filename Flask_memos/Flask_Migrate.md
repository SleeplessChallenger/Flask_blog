<h2>Here I tried to write how I've understood Flask Migrate</h2>

Generally migration helps to make tweaks to database and keep various versions of it

-`add pip install flask-migrate`

-`from flask_migrate import Migrate 
	migrate = Migrate(app, db)`

<h5>If you have project already, but don't have `migration`</h5>:
1. Go to directory where `__init__.py` (blog folder)

2. `export FLASK_APP=__init__.py`

3. flask db init

4. if project exists it'll write no changes are found
   => trick the system to think the db is empty

!! if you use unique features for particular database (instead of SQLITE)
   then it'll cause problems hence use features that are generall

5. SQLALCHEMY_DATABASE_URI=sqlite:/// flask db migrate

6. flask db stamp head

=> Everything should be OKAY

<h5>If you already have `migrations`</h5>:
1. `export FLASK_APP=__init__.py`

2. flask db migrate

3. flask db upgrade

-About errors
	if `cannot locate db`
	<ul>
		<li>remove db from folder</li>
		<li>flask db migrate</li>
		<li>flask db upgrade</li>
	</ul>

	if some other errors persist:
	<ul>
		<li>delete migrations folder</li>
		<li>then remove db</li>
		<li>return from 1 to 6</li>
	</ul>
