import requests
from config import api_key

def get_weather(lat, lon, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"  # For temperature in Celsius
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


lat = 40.806862
lon = -96.681679
api_key = api_key

weather_data = get_weather(lat, lon, api_key)

print(weather_data)

'''
if weather_data:
    print(f"Temperature: {weather_data['main']['temp']}°C")
    print(f"Description: {weather_data['weather'][0]['description']}")
    print(f"Humidity: {weather_data['main']['humidity']}%")
else:
    print("Failed to retrieve weather data.")
'''