from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def api_predict():

    data = request.get_json()

    age = int(data.get("age"))
    income = int(data.get("income"))
    bmi = float(data.get("bmi"))
    smoker = int(data.get("smoker"))

    # Risk Calculation
    risk_score = int((age * 200) + (bmi * 300) + (smoker * 10000))

    # Policy Logic
    if risk_score < 30000:
        policy = "Basic Health Insurance Plan"
        explanation = "Low health risk detected."
        benefits = ["Low premium", "Basic coverage", "Good for young users"]

    elif risk_score < 60000:
        policy = "Standard Health Insurance Plan"
        explanation = "Moderate health risk detected."
        benefits = ["Balanced premium", "Covers major diseases", "Doctor consultation"]

    else:
        policy = "Premium Comprehensive Plan"
        explanation = "High health risk detected."
        benefits = ["Full coverage", "Critical illness", "Complete protection"]

    # Suggestions
    suggestions = []

    if bmi > 25:
        suggestions.append("Maintain healthy BMI")
    if smoker == 1:
        suggestions.append("Quit smoking")
    if age > 45:
        suggestions.append("Regular health checkups")

    return jsonify({
        "risk_score": risk_score,
        "recommended_policy": policy,
        "explanation": explanation,
        "benefits": benefits,
        "suggestions": suggestions
    })


if __name__ == "__main__":
    app.run(debug=True, port=10000)