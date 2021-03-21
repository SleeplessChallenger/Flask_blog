from flask import Flask, Blueprint, render_template

calendar = Blueprint('calendar', __name__)


@calendar.route('/calendar')
def see_calen():
	return render_template('calendar.html')
