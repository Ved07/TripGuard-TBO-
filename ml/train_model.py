import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

os.makedirs("../model", exist_ok=True)

df = pd.read_csv("../data/trip_dataset.csv")

X = df.drop("risk", axis=1)
y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=150,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(model, "../model/risk_model.pkl")

print("Model Trained & Saved")
