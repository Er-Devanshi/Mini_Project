from flask import Flask, render_template, request, jsonify
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
# API endpoint for prediction
@app.route("/api/predict", methods=["POST"])
def api_predict():

    data = request.get_json()

    age = data["age"]
    income = data["income"]
    bmi = data["bmi"]
    smoker = data["smoker"]

    # Validation
    if age < 18 or age > 100:
        return jsonify({"error": "Age must be between 18 and 100"}), 400

    if bmi < 10 or bmi > 50:
        return jsonify({"error": "BMI must be between 10 and 50"}), 400

    if smoker not in [0,1]:
        return jsonify({"error": "Smoker must be 0 or 1"}), 400

    input_data = np.array([[age, income, bmi, smoker]])

    risk_score = model.predict(input_data)[0]

    if risk_score < 20000:
        policy = "Basic Health Insurance Plan"
        explanation = "Your profile shows low health risk based on age, BMI, and smoking habits."

    elif risk_score < 50000:
        policy = "Standard Health Insurance Plan"
        explanation = "Your profile indicates moderate health risk."

    else:
        policy = "Premium Comprehensive Plan"
        explanation = "Your profile shows higher health risk, so a comprehensive plan is recommended."

    return jsonify({
        "recommended_policy": policy,
        "risk_score": int(risk_score),
        "explanation": explanation
    })


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)