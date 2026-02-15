import requests
import joblib
import numpy as np
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not found in .env file")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "risk_model.pkl")
ROUTE_PATH = os.path.join(BASE_DIR, "data", "routes.json")

model = joblib.load(MODEL_PATH)

# ================= WEATHER =================

def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        rainfall = data.get("rain", {}).get("1h", 0)

        return {
            "temp": data["main"]["temp"],
            "rainfall": rainfall,
            "wind": data["wind"]["speed"],
            "visibility": data.get("visibility", 10000) / 1000,
            "condition": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }

    except Exception as e:
        print("Weather API Error:", e)
        return None

# ================= ROUTE =================

def get_route_data(source, destination):
    try:
        with open(ROUTE_PATH) as f:
            routes = json.load(f)

        key = f"{source.title()}-{destination.title()}"
        return routes.get(key, {
            "delay_probability": 50,
            "congestion_index": 50
        })
    except:
        return {
            "delay_probability": 50,
            "congestion_index": 50
        }


# ================= MAIN PIPELINE =================

def calculate_risk(source, destination, date):

    source_weather = get_weather(source)
    destination_weather = get_weather(destination)

    if not source_weather or not destination_weather:
        return 0, "Low", {}, {}, {}, []

    route_data = get_route_data(source, destination)

    travel_date = datetime.strptime(date, "%Y-%m-%d")

    features_dict = {
        "temp": destination_weather["temp"],
        "rainfall": destination_weather["rainfall"],
        "wind": destination_weather["wind"],
        "visibility": destination_weather["visibility"],
        "delay_prob": route_data["delay_probability"] / 100,   # FIXED SCALE
        "congestion": route_data["congestion_index"] / 100,    # FIXED SCALE
        "weekend": 1 if travel_date.weekday() >= 5 else 0,
        "month": travel_date.month,
        "festival": 1 if travel_date.month in [10, 11, 12] else 0
    }

    features = np.array([[
        features_dict["temp"],
        features_dict["rainfall"],
        features_dict["wind"],
        features_dict["visibility"],
        features_dict["delay_prob"],
        features_dict["congestion"],
        features_dict["weekend"],
        features_dict["month"],
        features_dict["festival"]
    ]])

    prediction = model.predict(features)[0]
    risk_score = round(max(0, min(prediction, 100)), 2)

    risk_level = "Low" if risk_score < 30 else "Medium" if risk_score < 60 else "High"

    breakdown = {
        "weather": min(int((features_dict["rainfall"] + features_dict["wind"]) * 2), 100),
        "route": int((features_dict["delay_prob"] + features_dict["congestion"]) * 50),
        "season": features_dict["weekend"] * 20
    }

    recommendations = generate_recommendation(features_dict, risk_score)

    return risk_score, risk_level, source_weather, destination_weather, breakdown, recommendations


# ================= RECOMMENDATION =================

def generate_recommendation(features, score):

    suggestions = []

    if features["rainfall"] > 10:
        suggestions.append("Heavy rainfall expected. Keep buffer time.")

    if features["wind"] > 25:
        suggestions.append("Strong winds may cause delays.")

    if features["congestion"] > 0.6:
        suggestions.append("High airport congestion predicted.")

    if features["weekend"] == 1:
        suggestions.append("Weekend traffic may increase delays.")

    if score > 70:
        suggestions.append("Consider rescheduling travel for lower risk.")

    if not suggestions:
        suggestions.append("Travel conditions look stable.")

    return suggestions


def get_feature_importance():
    importance = model.feature_importances_
    feature_names = [
        "Temperature", "Rainfall", "Wind Speed", "Visibility",
        "Route Delay", "Congestion", "Weekend", "Month", "Festival"
    ]
    return sorted(zip(feature_names, importance),
                  key=lambda x: x[1], reverse=True)[:3]
