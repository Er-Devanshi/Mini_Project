import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load data
data = pd.read_csv("../data/sample_data.csv")

X = data[["age", "income", "bmi", "smoker"]]
y = data["claims_amount"]

model = RandomForestRegressor()
model.fit(X, y)

joblib.dump(model, "risk_model.pkl")

print("Model trained and saved successfully!")