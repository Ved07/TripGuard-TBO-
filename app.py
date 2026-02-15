from flask import Flask, render_template, request
from engine.risk_engine import calculate_risk, get_feature_importance

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=["POST"])
def analyze():

    source = request.form.get("source")
    destination = request.form.get("destination")
    date = request.form.get("date")

    risk_score, risk_level, source_weather, destination_weather, breakdown, recommendations = calculate_risk(
        source, destination, date
    )

    top_features = get_feature_importance()

    return render_template(
        "result.html",
        source=source,
        destination=destination,
        date=date,
        risk_score=risk_score,
        risk_level=risk_level,
        source_weather=source_weather,
        destination_weather=destination_weather,
        breakdown=breakdown,
        recommendations=recommendations,
        top_features=top_features
    )

if __name__ == "__main__":
    app.run(debug=True)
