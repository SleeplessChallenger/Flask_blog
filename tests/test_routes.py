import unittest


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from blog import create_app, db
from blog.models import Post, User
from blog.config import config


class RoutesClass(unittest.TestCase):
	def setUp(self):
		self.app = create_app(config['testDB'])
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.client = self.app.test_client(use_cookies=True)

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_main_page(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		response = self.client.get('/random_page')
		self.assertEqual(response.status_code, 404)

	def test_account_actions(self):
		# register new user
		response = self.client.post('/register',
									 data={
									 'username': 'Kikuchi',
									 'email': 'kikuchi@gmail.com',
									 'password': '4322441414',
									 'confirm_password': '4322441414'
									 })
		self.assertEqual(response.status_code, 302)

		# login with the new user
		response = self.client.post('/login',
									data={
									'email': 'kikuchi@gmail.com',
									'password': '4322441414'
									}, follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		# check token sending
		user = User.query.filter_by(email='kikuchi@gmail.com').first()
		token = user.get_reset_token()
		response = self.client.get(f'confirm/{token}', follow_redirects=True)
		user.verify_token(token)
		self.assertEqual(response.status_code, 200)

		# log out
		response = self.client.post('/logout', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		# delete account
		response = self.client.get('/delete', follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		response = self.client.post('/delete', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

		user = User.query.filter_by(email='kikuchi@gmail.com').first()
		db.session.delete(user)
		db.session.commit()
		user = User.query.filter_by(email='kikuchi@gmail.com').first()
		self.assertIsNone(user)

	def test_weather_page(self):
		response = self.client.get('/start_page')
		self.assertEqual(response.status_code, 200)

	def test_without_registered(self):
		response = self.client.get('/delete')
		self.assertEqual(response.status_code, 302)
		response = self.client.get('/all_users')
		self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
	unittest.main()
