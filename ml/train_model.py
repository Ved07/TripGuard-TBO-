import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "risk_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "risk_model.pkl")

df = pd.read_csv(DATA_PATH)

X = df.drop("risk_score", axis=1)
y = df["risk_score"]

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

os.makedirs(os.path.join(BASE_DIR, "model"), exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("Model trained and saved successfully.")
