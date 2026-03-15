from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("models/risk_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def api_predict():

    data = request.get_json()

    age = data["age"]
    income = data["income"]
    bmi = data["bmi"]
    smoker = data["smoker"]

    # Input validation
    if age < 18 or age > 100:
        return jsonify({"error": "Age must be between 18 and 100"}), 400

    if bmi < 10 or bmi > 50:
        return jsonify({"error": "BMI must be between 10 and 50"}), 400

    if smoker not in [0, 1]:
        return jsonify({"error": "Smoker must be 0 or 1"}), 400

    # Prepare input for model
    input_data = np.array([[age, income, bmi, smoker]])

    # Predict risk score
    risk_score = model.predict(input_data)[0]

    # Policy recommendation logic
    if risk_score < 20000:
        policy = "Basic Health Insurance Plan"
        benefits = [
            "₹3L Coverage",
            "Free Doctor Consultation",
            "Medicine Coverage"
        ]
        explanation = "Your profile shows low health risk based on age, BMI and smoking habits."

    elif risk_score < 50000:
        policy = "Standard Health Insurance Plan"
        benefits = [
            "₹5L Coverage",
            "Hospitalization Coverage",
            "Doctor Consultation",
            "Medicine Coverage"
        ]
        explanation = "Your profile indicates moderate health risk."

    else:
        policy = "Premium Comprehensive Plan"
        benefits = [
            "₹10L Coverage",
            "All Hospital Expenses",
            "Free Annual Health Checkup",
            "Medicine + Doctor Consultation"
        ]
        explanation = "Your profile shows higher health risk, so a comprehensive plan is recommended."

    # Return API response
    return jsonify({
        "recommended_policy": policy,
        "risk_score": int(risk_score),
        "explanation": explanation,
        "benefits": benefits
    })


if __name__ == "__main__":
    app.run(debug=True)