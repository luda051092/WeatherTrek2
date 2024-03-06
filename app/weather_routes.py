from flask import Blueprint, jsonify, request, render_template
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
import logging
import sys
from retry_requests import retry
from city_routes import get_lat_lon  # Import the function from city_routes


weather_bp = Blueprint('weather', __name__)

# Configure logging to output to console
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Set up a cached session with requests_cache
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)

# Set up a retry mechanism with retry_requests
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

# Create an instance of the openmeteo_requests.Client using the retry-enabled session
openmeteo = openmeteo_requests.Client(session=retry_session)


WEATHER_API_KEY = 'KUbafkNI9CBq2ANGiX08DrEE6B0wCLuz'
WEATHER_API_URL = 'https://api.tomorrow.io/v4/weather/realtime'

def get_weather_icon_class(weather_code):
    # Map weather codes to Font Awesome icon classes
    icon_mapping = {
        'sunny': 'fas fa-sun',
        'cloudy': 'fas fa-cloud',
        'rainy': 'fas fa-cloud-showers-heavy',
        # Add more mappings as needed
    }
    
    return icon_mapping.get(weather_code, 'fas fa-question')

@weather_bp.route('/weather_data')
def weather_data():
    city_name = request.args.get('city_name')

    # Get latitude and longitude for the city
    latitude, longitude = get_lat_lon(city_name)

    # Get weather data
    params = {
        'location': f'{latitude},{longitude}',
        'apikey': WEATHER_API_KEY,
        'fields': 'temperature,humidity,weatherCode,windSpeed,windDirection,uvIndex,precipitationIntensity',
    }

    response_weather = requests.get(WEATHER_API_URL, params=params)

    if response_weather.status_code == 200:
        weather_data = response_weather.json().get("data", {}).get("values", {})
        weather_code = weather_data.get('weatherCode', '')
        icon_class = get_weather_icon_class(weather_code)
    else:
        return jsonify({"error": f"Failed to fetch weather data. Status code: {response_weather.status_code}"})

    return render_template('index.html', city_name=city_name, weather_data=weather_data, icon_class=icon_class)

