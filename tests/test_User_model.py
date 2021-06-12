import unittest
from time import sleep
from unittest.mock import patch


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from blog import create_app, db
from blog.models import User
from blog.config import config


class UserTest(unittest.TestCase):
	def setUp(self):
		self.app = create_app(config['testDB'])
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.user = User(username='Haruka', email='haruka@yahoo.com',
				 password='just some letters', image_file='Night view.png')
		db.session.add(self.user)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_model_repr(self):
		self.assertEqual(repr(self.user), "User: Haruka, haruka@yahoo.com, Night view.png")

	def test_token_valid(self):
		token = self.user.generate_confirmation_token()
		self.assertTrue(self.user.verify_token(token))

	def test_token_invalid(self):
		token = self.user.generate_confirmation_token(expires_sec=0.2)
		sleep(1)
		self.assertFalse(self.user.verify_token(token))

	def test_token_difference(self):
		user_test = User(username='Kobayashi', email='kobayashi@gmail.com',
				 password='random password', image_file='Day view.jpg')
		db.session.add(user_test)
		db.session.commit()
		token1 = self.user.get_reset_token()
		token2 = user_test.get_reset_token()
		self.assertNotEqual(token1, token2)

	def test_token_from_another_user(self):
		user_test = User(username='Kobayashi', email='kobayashi@gmail.com',
				 password='random password', image_file='Day view.jpg')
		db.session.add(user_test)
		db.session.commit()
		token = user_test.get_reset_token()
		self.assertFalse(self.user.verify_token(token))

	def test_follow_unfollow_feature(self):
		user_test = User(username='Kobayashi', email='kobayashi@gmail.com',
				 password='random password', image_file='Day view.jpg')
		db.session.add(user_test)
		db.session.commit()

		self.assertFalse(self.user.is_following(user_test))
		self.user.follow(user_test)
		self.assertTrue(self.user.is_following(user_test))
		self.user.unfollow(user_test)
		self.assertFalse(self.user.is_following(user_test))

		user_test.follow(self.user)
		self.assertTrue(self.user.is_followed_by(user_test))
		user_test.unfollow(self.user)
		self.assertFalse(self.user.is_followed_by(user_test))

	@patch('blog.models.User.to_json')
	def test_json(self, mock_obj):
		mock_obj.return_value = {
			'url': '/api/v1/users/',
			'username': 'Haruka',
			'posts_url': None
			}
		expected_keys = ['url', 'username', 'posts_url']
		self.assertEqual(sorted(mock_obj.return_value.keys()), sorted(expected_keys))
		self.assertEqual(sorted((self.user.to_json())), sorted(expected_keys))


if __name__ == '__main__':
	unittest.main()
