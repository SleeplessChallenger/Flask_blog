from . import api
from flask import jsonify
from blog.validation_error import ValidationError


'''
To deal with 'content negotiation' [which format
of response to give to the client API from server]
we tweak our error_handlers

This new version of the error handler checks the Accept request header.

Functions in this api will invoke view_functions in errors folder
and use them to generate responses
'''

class ValidationError(ValueError):
    pass

def not_rights(msg):
	response = jsonify({'error': 'forbidden route',
						'message': msg})
	response.status_code = 403
	return response

def bad_request(msg):
	response = jsonify({'error': 'bad request',
						'message': msg})
	response.status_code = 400
	return response

def not_authorized(msg):
	response = jsonify({'error': 'unathorized',
						'message': msg})
	response.status_code = 401
	return response

@api.errorhandler(ValidationError)
def validation_error(msg):
	return bad_request(msg.args[0]) 


'''The application now needs to handle this exception by providing the
appropriate response to the client. To avoid having to add exception-catching
code in view functions, a global exception handler can be installed using
Flask’s errorhandler decorator'''