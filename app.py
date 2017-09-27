from decimal import Decimal
from flask import flash, Flask, render_template, request
from flask_bootstrap import Bootstrap
from wit import Wit
import requests

WIT_ACCESS_TOKEN = '75ACGKG2S3TD2BCG42GOFNH5OEKGZLL4'  # from https://wit.ai/aroder/MyFirstApp/settings
WEATHER_API_KEY = '50664a4923b14001ba7220326172709'

app = Flask('__name__')
Bootstrap(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'super secret key'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    msg = request.form['message']
    wit_client = Wit(WIT_ACCESS_TOKEN)
    resp = wit_client.message(msg)
    intent = resp['entities']['intent'][0]['value']
    location = resp['entities']['location'][0]['value'] if resp['entities']['location'] is not None else 'Parker, CO'

    # if (intent is 'weather'):
    req = f'http://api.apixu.com/v1/current.json?key={WEATHER_API_KEY}&q={location}'
    r = requests.get(req)

    w = r.json()

    temp = w['current']['temp_f']
    wind = w['current']['wind_mph']
    direction = w['current']['wind_dir']

    weather_lookup = {
        'message': msg,
        'bot_response': f'The bot understood the intent "{intent}"',
        'weather': f'The current temperature in {location} is {temp} F, with winds from the {direction} at {wind} MPH.'
    }
    #flash('Message sent to bot and weather retrieved')
    return render_template('index.html', weather_lookup=weather_lookup)
