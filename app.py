from flask import Flask, request
from flask_cors import CORS
from api.weather import Weather

app = Flask(__name__)
CORS(app)

api_key = 'f819e16273820cd7df6d1bfee66a7bda'
weather = Weather(api_key)
print(weather)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/weather')
def get_weather():
    # get the location from the query parameter
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'location parameter is missing'}), 400
    
    return weather.get_current_weather(location)


@app.route('/forecast')
def get_forecast():
    # get the location from the query parameter
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'location parameter is missing'}), 400

    return weather.get_forecast(location)

 