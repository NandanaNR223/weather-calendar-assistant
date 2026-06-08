import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Mishawaka"

url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=1&aqi=no&alerts=no"

response = requests.get(url)
data = response.json()

location = data["location"]["name"]
current_temp = data["current"]["temp_c"]
condition = data["current"]["condition"]["text"]

print(f"Weather in {location}:")
print(f"Temperature: {current_temp}°C")
print(f"Condition: {condition}")
