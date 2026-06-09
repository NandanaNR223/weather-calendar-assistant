import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Mishawaka"

ACTIVITY_RULES = {
    "run" : {"hot_temp" : 32, "wind_limit" : 30},
    "jog" : {"hot_temp" : 32, "wind_limit" : 30},
    "walk" : {"hot_temp" : 32, "wind_limit" : 30},
    "hike" : {"hot_temp" : 32, "wind_limit" : 30},
    "cycling" : {"hot_temp": 30, "wind_limit" : 35},
    "picnic" : {"hot_temp" : 35, "wind_limit" : 25},
    "football" : {"hot_temp" : 32, "wind_limit" : 30},
    "tennis" : {"hot_temp" : 32, "wind_limit" : 30},
    "gardening" : {"hot_temp" : 35, "wind_limit" : 25}
}

def get_weather_data():
    url = (
        f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=1&aqi=no&alerts=no"
    )

    response = requests.get(url)
    return response.json()

def is_valid_time_format(target_time):
    return len(target_time) == 5 and target_time[2] == ":" and target_time[:2].isdigit() and target_time[3:].isdigit()

def get_forecast_for_time(hours, target_time):
    for hour in hours:
        if target_time in hour["time"]:
            return hour
    
    return None

def generate_recommendation(activity, forecast):
    activity = activity.lower()

    rain_chance = forecast["chance_of_rain"]
    temp_c = forecast["temp_c"]
    wind_kph = forecast["wind_kph"]

    if rain_chance >= 70:
        return f"It may rain during your {activity}. Carry rain gear or consider rescheduling."

    if activity not in ACTIVITY_RULES:
        return "Activity not recognized. Check weather details before heading out."
    
    rules = ACTIVITY_RULES[activity]

    if temp_c >= rules["hot_temp"]:
        return f"It may be too hot for your {activity}. Carry water and stay hydrated."
    
    if wind_kph >= rules["wind_limit"]:
        return f"It may be windy for your {activity}."
        
    return f"Weather looks fine for your {activity}."

def main():
    activity = input("Enter your activity: ").lower()
    target_time = input("Enter a time in 24-hour format (HH:MM): ")

    if not is_valid_time_format(target_time):
        print("Invalid time format. Please enter time like so - 17:00")
        return
    
    data = get_weather_data()
    hours = data["forecast"]["forecastday"][0]["hour"]

    forecast = get_forecast_for_time(hours, target_time)

    if forecast:
        print(f"\nForecast for {target_time} in {CITY}:")
        print(f"Temperature: {forecast["temp_c"]}°C")
        print(f"Condition: {forecast["condition"]["text"]}")
        print(f"Wind: {forecast["wind_kph"]} km/h")
        print(f"Rain Chance: {forecast["chance_of_rain"]}%")
        
        recommendation = generate_recommendation(activity, forecast)
        print(f"Recommendation: {recommendation}")

    else:
        print(f"No forecasr found {target_time}.")


if __name__ == "__main__":
    main()