import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog import mail


def save_pic(pics):
	random_name = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(pics.filename)
	new_name = random_name + f_ext
	pic_path = os.path.join(current_app.root_path, 'static/pics', new_name)
	# pics.save(pic_path) => we'll save resized one

	# in .css we can place max size of image
	# in our case it's 125px
	# => everything > 125 is no use 
	# and slows speed of site

	size = (125, 125)
	file = Image.open(pics)
	file.thumbnail(size)
	file.save(pic_path)

	return new_name

def send_email(user):
	token = user.get_reset_token() # get token of current user
	msg = Message('Password reser request', sender='noreply@gmail.com',
				   recipients=[user.email])
	msg.body = f'''To reset your password follow the provided link:
{url_for('users.reset_token', user=user, token=token, _external=True)}

If you didn't request this email then ignore it.
ありがとうございます
'''
	mail.send(msg)

def send_confirm_email(user):
	token_mail = user.generate_confirmation_token()
	msg = Message('Please, confirm your account', sender='noreply@gmail.com',
				   recipients=[user.email])
	msg.body = f'''To verify your account, please follow provided link:
{url_for('users.confirm', token=token_mail, _external=True)}
	
	失礼します
'''
	mail.send(msg)


# def send_email(to, subject, template, **kwargs):
#     app = current_app._get_current_object()
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
#                   sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr