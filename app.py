from flask import Flask, render_template, request
from engine.risk_engine import (
    get_weather,
    predict_risk,
    get_risk_level,
    generate_recommendation,
    get_feature_importance
)

from datetime import datetime
import random

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=["POST"])
def analyze():

    source = request.form.get("source")
    destination = request.form.get("destination")
    date = request.form.get("date")

    if not source or not destination or not date:
        return "Missing input fields", 400

    # 🔹 Convert date
    travel_date = datetime.strptime(date, "%Y-%m-%d")

    # 🌦 Fetch REAL Weather
    source_weather = get_weather(source)
    destination_weather = get_weather(destination)

    # If API fails
    if not source_weather or not destination_weather:
        return "Weather API Error. Check city name.", 500

    # 🌧 Rainfall (if not present)
    rainfall = source_weather.get("rainfall", 0)

    # 🧠 Build ML Feature Vector
    features = {
        "temp": source_weather["temp"],
        "rainfall": rainfall,
        "wind": source_weather["wind"],
        "visibility": source_weather["visibility"],
        "delay_prob": random.uniform(0.2, 0.7),   # Temporary until real route dataset
        "congestion": random.uniform(0.3, 0.9),   # Temporary until real route dataset
        "weekend": 1 if travel_date.weekday() >= 5 else 0,
        "month": travel_date.month,
        "festival": 0
    }

    # 🔮 ML Risk Prediction
    risk_score = predict_risk(features)

    # 🎯 Risk Level
    risk_level = get_risk_level(risk_score)

    # 📊 Feature Importance (Explainability)
    top_features = get_feature_importance()

    # 💡 Intelligent Recommendation
    recommendations = generate_recommendation(features, risk_score)

    # 📈 Risk Breakdown for UI Bars
    breakdown = {
        "weather": min(int((features["rainfall"] + features["wind"]) * 2), 100),
        "route": int(features["delay_prob"] * 100),
        "season": features["weekend"] * 20
    }

    return render_template(
        "result.html",
        source=source,
        destination=destination,
        date=date,
        risk_score=risk_score,
        risk_level=risk_level,
        recommendations=recommendations,
        source_weather=source_weather,
        destination_weather=destination_weather,
        breakdown=breakdown,
        top_features=top_features
    )


if __name__ == "__main__":
    app.run(debug=True)
