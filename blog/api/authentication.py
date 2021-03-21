from flask import  g, jsonify
from flask_httpauth import HTTPBasicAuth
from blog.api.errors import not_authorized, not_rights
from blog.api import api
import bcrypt
from blog.models import User

auth = HTTPBasicAuth()
# we initialize it here because this 'type' of user
# authentication will only be used in the API Blueprint


@auth.verify_password
def verify_password(email_token, password):
	if email_token == '':
		return False
	'''
	In this new version, the first authentication argument can be the email
	address or an authentication token. If this field is blank, an anonymous
	user is assumed, as before. If the password is blank, then the email_or_token
	field is assumed to be a token and validated as such. If both fields are nonempty
	then regular email and password authentication is assumed

	To give view functions the ability to distinguish between the two
	authentication methods a g.token_used variable is added
	'''	
	if password == '':
		g.current_user = User.verify_reset_token(email_token)
		g.token_used = True
		return g.current_user is not None
	user = User.query.filter_by(email=email_token).first()
	if user is None:
		return False
	g.current_user = user
	g.token_used = False
	'''
	The authentication callback saves the authenticated user in Flask’s
	g context variable so that the view function can access it later.

	In this logic we block unauthorized user
	(they carry empty 'strings')

	'''
	return bcrypt.check_password_hash(password, user.password)


'''
When the authentication credentials are invalid, the server returns a 401
status code response to the client. Flask-HTTPAuth generates a response
with this status code by default, but to ensure that the response is consistent
with other errors returned by the API, the error response can be customized
'''
@auth.error_handler
def auth_401():
	return unauthorized('Invalid credentials')

'''Blueprint.before_request is called before each request within the blueprint.
If you want to call it before all blueprints, please use before_app_request.'''
@api.before_request
@auth.login_required
def before_request():
	if not g.current_user.is_anonymous and\
	   not g.current_user.confirmed:
		return not_rights('Unconfirmed account')

# to return authentication tokens to the client
@api.route('/tokens/', methods=['POST'])
def get_token():
	if g.current_user.is_anonymous or\
	   g.token_used:
	   return not_authorized('Invalid credetentials')
	return jsonify({'token': g.current_user.get_reset_token})
'''
To prevent clients from authenticating to this route using a previously obtained
token instead of an email address and pass‐ word, the g.token_used variable is checked,
and requests authenticated with a token are rejected. The purpose of this is to prevent
users from bypassing the token expira‐ tion by requesting a new token using the old
token as authentication
'''
