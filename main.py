import os
import requests
from dotenv import load_dotenv
from rapidfuzz import fuzz
from activity_similarity import classify_by_similarity
from calendar_api import get_calendar_events

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

OUTDOOR_EXERCISE = {
    "exercise" : [
        "walk", "run", "jog", "hike", "bike", "cycling", "cardio", "training", "exercise", "workout"
    ],
    "outdoor_places" : [
        "park", "beach", "trail", "campus", "picnic"
    ]
}

ERRANDS = {
    "shopping" : [
        "grocery", "groceries", "shopping", "market", "store"
    ],
    "services" : [
        "pharmacy", "bank", "post", "office", "laundry", "medicine", "prescription",
        "medication"
    ]
}

INDOOR = {
    "appointments" : [
        "meeting", "class", "doctor", "appointmet", "lecture"
    ],
    "indoor_places" : [
        "gym", "library", "work", "study"
    ]
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

def fuzzy_match(word, keywords, threshold=75):
    for keyword in keywords:
        score = fuzz.ratio(word, keyword)

        if score >= threshold:
            return True
        
    return False

def normalize_text(text):
    text = text.lower().strip()
    punctuation = [".",",","!","?",":",";","-","_"]
    
    for mark in punctuation:
        text = text.replace(mark, " ")
    
    text = " ".join(text.split())
    return text

def classify_activity(activity):
    result = classify_by_similarity(activity)

    if result["best_match"] is not None:
        print(f"\nMatched with: {result["best_match"]}")
        print(f"Similarity score: {result["score"]:.2f}")
    else:
        print("No confident activity match found")
    
    return result["category"]

def generate_recommendation(activity, activity_type, forecast):
    activity = activity.lower()

    rain_chance = forecast["chance_of_rain"]
    temp_c = forecast["temp_c"]
    wind_kph = forecast["wind_kph"]

    if rain_chance >= 70:
        return f"It may rain during your {activity}. Carry rain gear or consider rescheduling."

    if activity_type == "outdoor":
        rules = ACTIVITY_RULES["walk"]
    
    elif activity_type == "errand":
        rules = ACTIVITY_RULES["walk"]
    
    elif activity_type == "indoor":
        return "This looks like an indoor activity, so weather may not affect it much."
    
    else:
        return "Activity not recognized. Check weather details before heading out."

    if temp_c >= rules["hot_temp"]:
        return f"It may be too hot for your {activity}. Carry water and stay hydrated."
    
    if wind_kph >= rules["wind_limit"]:
        return f"It may be windy for your {activity}."
        
    return f"Weather looks fine for your {activity}."

def process_activity(activity, target_time, hours):
    activity_type = classify_activity(activity)
    forecast = get_forecast_for_time(hours, target_time)

    if forecast is None:
        print(f"\n{activity} at {target_time}")
        print("Sorry, I couldn't find weather data for that time.")
        return 
    
    recommendation = generate_recommendation(activity, activity_type, forecast)

    print(f"\n{activity} at {target_time}")
    print(f"Category: {activity_type}")
    print(recommendation)

def main():
    data = get_weather_data()
    hours = data["forecast"]["forecastday"][0]["hour"]

    calendar_events = get_calendar_events()
    
    for event in calendar_events:
        process_activity(event["activity"], event["time"], hours)


if __name__ == "__main__":
    main()