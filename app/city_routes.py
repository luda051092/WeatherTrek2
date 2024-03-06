from flask import Blueprint, jsonify, request, render_template
import requests


city_bp = Blueprint('city', __name__)

GEOCODING_API_KEY = ''
GEOCODING_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


def get_lat_lon(city_name):
    params = {
        'address': city_name,
        'key': GEOCODING_API_KEY,
    }

    response = requests.get(GEOCODING_API_URL, params=params)

    if response.status_code == 200:
        location_data = response.json().get('results', [])[0].get('geometry', {}).get('location', {})
        latitude = location_data.get('lat', '42.3478')  # Default to Boston if not found
        longitude = location_data.get('lng', '-71.0828')  # Default to Boston if not found
        return latitude, longitude
    else:
        return '42.3478', '-71.0828'  # Default to Boston if geocoding fails

def get_city_data(api_key, city_name):
    url = f"https://api.api-ninjas.com/v1/city?name={city_name}"
    headers = {'X-Api-Key': api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        city_data_list = response.json()
        if city_data_list:
            # Assuming the first item in the list contains the desired data
            city_data = city_data_list[0]
            return city_data
        else:
            print(f"No data available for {city_name}.")
            return None
    else:
        print(f"Failed to fetch data for {city_name}. Status code: {response.status_code}")
        return None


@city_bp.route('/city_data')
def city_data():
    city_name = request.args.get('city_name', 'Boston')  # Default to Boston if city name not provided


    # Get latitude and longitude for the city
    latitude, longitude = get_lat_lon(city_name)

     # Get city data
    city_data = get_city_data(api_key='T7EWh4zGbH5Rg/p+lCTWLQ==s7Yf90FoIPwZrXyZ', city_name=city_name)

    return render_template('index.html', city_name=city_name, city_data=city_data)

if __name__ == '__main__':
    app.run(debug=True)
