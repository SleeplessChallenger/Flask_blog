import requests
from flask import (Flask, render_template, request, 
				   Blueprint, current_app)
import os
weather = Blueprint('weather', __name__)


@weather.route('/start_page')
def weather_home():
	return render_template('weather.html')

@weather.route('/city', methods=['POST'])
def city_input():
	# api_key = current_app.config.get('API_KEY')
	# due to issues with environment variables
	# regarded 'api_key' I hardcoded it here
	api_key = '1092b14452b8a9e73d812df95985bc6f'
	if not api_key:
		return render_template('errors/403.html')

	city = request.form.get('city_name')

	url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
	response = requests.get(url).json()

	if response.get('cod') != 200:
		msg = response.get('message')
		return render_template('errors/invalid.html', msg=msg)

	# temp_kelvin = response['main']['temp']
	temp_kelvin = response.get('main', None).get('temp', None)
	temp_kelvin_feels = response.get('main', None).get('feels_like', None)
	weather_way = response.get('weather', None)[0].get('main', None)
	if temp_kelvin and temp_kelvin_feels:
		temp_celsius = round(temp_kelvin - 273.15, 2)
		temp_celsius_feels = round(temp_kelvin_feels - 273.15, 2)
		return render_template('results.html', temp=temp_celsius,
								location=city, temp_feels=temp_celsius_feels,
								weather=weather_way)
	return render_template('errors/invalid.html')


# Success:

# {"coord":{"lon":139.6917,"lat":35.6895}, "weather":[{"id":801,"main":"Clouds",\
# "description":"few clouds","icon":"02n"}], "base":"stations",  "main":{"temp":287.12,\
# "feels_like":283.28,"temp_min":286.48,"temp_max":287.59,"pressure":1007,"humidity":58},\
# "visibility":10000,"wind":{"speed":4.12,"deg":310},"clouds":{"all":20},"dt":1615912431,\
# "sys":{"type":1,"id":8074,"country":"JP","sunrise":1615927781,"sunset":1615970983},\
# "timezone":32400,"id":1850144,"name":"Tokyo","cod":200}

# Failure:

# {"cod":401, "message": "Invalid API key. Please see http://openweathermap.org/faq#error401\
# for more info."}



