import pandas as pd
import numpy as np
import random
import os

rows = 3000
data = []

for _ in range(rows):

    temp = random.uniform(10, 45)
    rainfall = random.uniform(0, 50)
    wind = random.uniform(0, 40)
    visibility = random.uniform(1, 10)

    delay_prob = random.uniform(0, 1)      # 0–1 scale
    congestion = random.uniform(0, 1)      # 0–1 scale

    weekend = random.randint(0, 1)
    month = random.randint(1, 12)
    festival = random.randint(0, 1)

    # Proper 0–100 target
    risk = (
        rainfall * 1.5 +
        wind * 1.2 +
        (1 - visibility/10) * 25 +
        delay_prob * 40 +
        congestion * 35 +
        weekend * 8 +
        festival * 15
    )

    risk = min(max(risk, 0), 100)

    data.append([
        temp, rainfall, wind, visibility,
        delay_prob, congestion,
        weekend, month, festival,
        risk
    ])

columns = [
    "temp", "rainfall", "wind", "visibility",
    "delay_prob", "congestion",
    "weekend", "month", "festival",
    "risk_score"
]

df = pd.DataFrame(data, columns=columns)

os.makedirs("../data", exist_ok=True)
df.to_csv("../data/risk_dataset.csv", index=False)

print("Dataset generated successfully.")
