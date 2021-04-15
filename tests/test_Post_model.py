import unittest
from dateutil import parser
from unittest.mock import patch


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from blog import create_app, db
from blog.models import Post, User
from blog.config import config


class PostTest(unittest.TestCase):
	def setUp(self):
		self.app = create_app(config['testDB'])
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.user = User(username='Takada', email='takada@gmail.com',
						 password='just some letters', image_file='Night view.png')
		db.session.add(self.user)
		db.session.commit()
		self.post = Post(title='Random post', date_posted=parser.parse("2020 05 17 12:00AM"),
				 		 content='Some words', user_id=self.user.id)
		db.session.add(self.post)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_model_repr(self):
		self.assertEqual(repr(self.post), "Post: Random post, 2020-05-17 00:00:00")

	@patch('blog.models.Post.to_json')
	def test_json(self, mock_obj):
		mock_obj.return_value = {
					'url': None,
					'body': 'Some words',
					'body_html': None,
					'date_posted': '2020-05-17 00:00:00',
					'author_url': None
		}
		expected_keys = ['url', 'body', 'body_html', 'date_posted', 'author_url']
		self.assertEqual(sorted(mock_obj.return_value.keys()), sorted(expected_keys))

	def test_backref_id(self):
		self.assertEqual(self.post.user_id, self.user.id)

	def test_backref_db(self):
		self.assertEqual(self.user.posts[0], self.post)


if __name__ == '__main__':
	unittest.main()
