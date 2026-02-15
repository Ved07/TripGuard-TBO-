import requests
import joblib
import numpy as np
import os

# ==============================
# 🔐 CONFIGURATION
# ==============================

API_KEY = "75b3d4fa03ed964982c2325e04d0b433"  # 🔥 Replace with your real API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Get root project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build correct model path
MODEL_PATH = os.path.join(BASE_DIR, "model", "risk_model.pkl")

# Load model
model = joblib.load(MODEL_PATH)


# ==============================
# 🌦 WEATHER FETCH FUNCTION
# ==============================

def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            return None

        # Extract rainfall safely
        rainfall = 0
        if "rain" in data:
            rainfall = data["rain"].get("1h", 0)

        return {
            "temp": data["main"]["temp"],
            "rainfall": rainfall,
            "wind": data["wind"]["speed"],
            "visibility": data.get("visibility", 10000) / 1000,  # convert to km
            "condition": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }

    except Exception as e:
        print("Weather API Error:", e)
        return None


# ==============================
# 🤖 ML RISK PREDICTION
# ==============================

def predict_risk(features_dict):

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

    return round(min(prediction, 100), 2)


# ==============================
# 🎯 RISK LEVEL CLASSIFICATION
# ==============================

def get_risk_level(score):

    if score < 30:
        return "Low"
    elif score < 60:
        return "Medium"
    else:
        return "High"


# ==============================
# 📊 FEATURE IMPORTANCE
# ==============================

def get_feature_importance():

    importance = model.feature_importances_

    feature_names = [
        "Temperature",
        "Rainfall",
        "Wind Speed",
        "Visibility",
        "Route Delay Probability",
        "Airport Congestion",
        "Weekend",
        "Month",
        "Festival"
    ]

    sorted_features = sorted(
        zip(feature_names, importance),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_features[:3]  # Top 3 contributors


# ==============================
# 💡 SMART RECOMMENDATION ENGINE
# ==============================

def generate_recommendation(features, score):

    suggestions = []

    if features["rainfall"] > 10:
        suggestions.append("Heavy rainfall expected. Keep extra buffer time.")

    if features["wind"] > 30:
        suggestions.append("Strong winds may cause operational delays.")

    if features["congestion"] > 0.7:
        suggestions.append("High airport congestion predicted.")

    if features["weekend"] == 1:
        suggestions.append("Weekend traffic may increase delays.")

    if score > 70:
        suggestions.append("Consider rescheduling travel for lower risk.")

    if not suggestions:
        suggestions.append("Weather and route conditions look stable.")

    return suggestions
