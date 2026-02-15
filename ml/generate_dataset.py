import pandas as pd
import numpy as np
import os

os.makedirs("../data", exist_ok=True)

data = []

for _ in range(3000):
    temp = np.random.uniform(5, 45)
    rainfall = np.random.uniform(0, 30)
    wind = np.random.uniform(0, 60)
    visibility = np.random.uniform(1, 10)
    delay_prob = np.random.uniform(0.1, 0.8)
    congestion = np.random.uniform(0.2, 0.9)
    weekend = np.random.choice([0, 1])
    month = np.random.randint(1, 13)
    festival = np.random.choice([0, 1], p=[0.85, 0.15])

    risk = (
        rainfall * 1.8 +
        wind * 0.8 +
        (10 - visibility) * 4 +
        delay_prob * 40 +
        congestion * 35 +
        weekend * 8 +
        festival * 12
    )

    risk = min(risk, 100)

    data.append([
        temp, rainfall, wind, visibility,
        delay_prob, congestion,
        weekend, month, festival,
        risk
    ])

df = pd.DataFrame(data, columns=[
    "temp","rainfall","wind","visibility",
    "delay_prob","congestion",
    "weekend","month","festival",
    "risk"
])

df.to_csv("../data/trip_dataset.csv", index=False)
print("Dataset Generated Successfully")
