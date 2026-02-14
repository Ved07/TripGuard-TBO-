from flask import Flask, render_template, request
from engine.risk_engine import calculate_risk
from engine.suggestion_engine import generate_suggestion

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=["POST"])
def analyze():
    source = request.form.get("source")
    destination = request.form.get("destination")
    date = request.form.get("date")

    # Call risk engine
    risk_score, risk_level = calculate_risk(source, destination, date)

    # Call suggestion engine
    suggestion = generate_suggestion(risk_level)

    return render_template("result.html",
                           source=source,
                           destination=destination,
                           date=date,
                           risk_score=risk_score,
                           risk_level=risk_level,
                           suggestion=suggestion)

if __name__ == "__main__":
    app.run(debug=True)
