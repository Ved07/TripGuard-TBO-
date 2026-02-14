import random

def calculate_risk(source, destination, date):
    # Hackathon dummy logic
    weather_risk = random.randint(10, 50)
    delay_risk = random.randint(10, 50)

    total_risk = weather_risk + delay_risk

    if total_risk < 40:
        level = "Low"
    elif total_risk < 70:
        level = "Medium"
    else:
        level = "High"

    return total_risk, level
