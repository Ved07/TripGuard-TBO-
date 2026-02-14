import json
import os
import requests
from datetime import datetime
from config import API_KEY, BASE_WEATHER_URL

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DELAYS_FILE = os.path.join(BASE_DIR, "data", "delays.json")
SEASON_FILE = os.path.join(BASE_DIR, "data", "season.json")


def load_json(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


# 🔥 Fetch Live Weather
# Note -> This is current weather condition. For a real app, we would want to fetch forecast data for the travel date.
def get_weather_data(city):

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_WEATHER_URL, params=params)

    if response.status_code != 200:
        return {
            "temp": "N/A",
            "condition": "Unknown",
            "icon": "",
            "risk": 20
        }

    data = response.json()

    temp = data["main"]["temp"]
    condition = data["weather"][0]["main"]
    icon = data["weather"][0]["icon"]

    # Convert condition → risk score
    if condition == "Clear":
        risk = 5
    elif condition == "Clouds":
        risk = 10
    elif condition == "Rain":
        risk = 25
    elif condition == "Drizzle":
        risk = 20
    elif condition == "Thunderstorm":
        risk = 40
    elif condition == "Snow":
        risk = 35
    else:
        risk = 15

    return {
        "temp": temp,
        "condition": condition,
        "icon": icon,
        "risk": risk
    }



def calculate_risk(source, destination, date):

    delay_data = load_json(DELAYS_FILE)
    season_data = load_json(SEASON_FILE)

    # 🌦 Get Weather for BOTH cities
    source_weather = get_weather_data(source)
    destination_weather = get_weather_data(destination)

    weather_risk = destination_weather["risk"]

    # Route Risk
    route_key = f"{source}-{destination}"
    route_risk = delay_data.get(route_key, 15)

    # Weekend Risk
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    if date_obj.weekday() >= 5:
        season_risk = season_data["weekend"]
    else:
        season_risk = season_data["weekday"]

        total_risk = (
        weather_risk * 0.5 +
        route_risk * 0.4 +
        season_risk * 0.1
    )
    # Total risk is a weighted sum of all factors
    total_risk = round(total_risk, 2)

    if total_risk < 20:
        level = "Low"
    elif total_risk < 35:
        level = "Medium"
    else:
        level = "High"

    breakdown = {
        "weather": round(weather_risk, 2),
        "route": round(route_risk, 2),
        "season": round(season_risk, 2)
    }

    return total_risk, level, source_weather, destination_weather, breakdown

