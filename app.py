from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# -------------------------------
# Risk Calculation (NO MODEL)
# -------------------------------
def calculate_risk(age, income, bmi, smoker):
    risk = 0

    # Basic factors
    risk += age * 100
    risk += bmi * 200

    if smoker == 1:
        risk += 20000

    if income > 50000:
        risk += 10000

    return risk


# -------------------------------
# Policy Recommendation
# -------------------------------
def recommend_policies(risk_score):
    
    if risk_score < 30000:
        return [
            "Basic Health Insurance Plan",
            "Family Starter Plan",
            "Young Care Plan",
            "Preventive Care Plan"
        ]
    
    elif risk_score < 60000:
        return [
            "Standard Health Insurance Plan",
            "Family Protection Plan",
            "Smart Health Plan",
            "Comprehensive Care Plan"
        ]
    
    else:
        return [
            "Premium Comprehensive Plan",
            "Critical Illness Cover",
            "Elite Health Plan",
            "Complete Protection Plan"
        ]


# -------------------------------
# Suggestions Generator
# -------------------------------
def generate_suggestions(age, bmi, smoker):
    suggestions = []

    if bmi > 25:
        suggestions.append("Maintain a healthy BMI")

    if smoker == 1:
        suggestions.append("Quit smoking")

    if age > 45:
        suggestions.append("Go for regular health checkups")

    if not suggestions:
        suggestions.append("Keep maintaining a healthy lifestyle")

    return suggestions


# -------------------------------
# Home Route
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# API Route
# -------------------------------
@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        age = int(data["age"])
        income = int(data["income"])
        bmi = float(data["bmi"])
        smoker = int(data["smoker"])

        # Calculate risk
        risk_score = calculate_risk(age, income, bmi, smoker)

        # Get policies
        policies = recommend_policies(risk_score)

        # Suggestions
        suggestions = generate_suggestions(age, bmi, smoker)

        # Risk level
        if risk_score < 30000:
            risk_level = "Low Risk"
        elif risk_score < 60000:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

        return jsonify({
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "recommended_policy": policies[0],
            "all_policies": policies,
            "explanation": f"Based on your profile, you fall under {risk_level}.",
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=10000)