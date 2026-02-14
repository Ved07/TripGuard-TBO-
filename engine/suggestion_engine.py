def generate_suggestion(risk_level):

    if risk_level == "Low":
        return "Travel looks safe. Proceed as planned."

    elif risk_level == "Medium":
        return "Monitor updates. Consider flexible booking options."

    else:
        return "High risk detected. Consider alternate date or route."
