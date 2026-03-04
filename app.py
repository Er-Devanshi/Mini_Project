from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("models/risk_model.pkl")

def recommend_policy(risk_score):
    if risk_score < 30000:
        return "Basic Health Insurance Plan"
    elif risk_score < 60000:
        return "Standard Health Insurance Plan"
    else:
        return "Premium Comprehensive Plan"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        age = int(request.form["age"])
        income = int(request.form["income"])
        bmi = float(request.form["bmi"])
        smoker = int(request.form["smoker"])

        input_data = np.array([[age, income, bmi, smoker]])

        risk_score = model.predict(input_data)[0]

        policy = recommend_policy(risk_score)

        risk_percent = round((risk_score / 100000) * 100, 2)

        return render_template("index.html",
                               policy=policy,
                               risk_score=round(risk_score, 2),
                               risk_percent=risk_percent)

    return render_template("index.html")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)