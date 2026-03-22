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

    # BMI based
    if bmi > 25:
        suggestions.append("⚠️ Your BMI is high. Try regular exercise and a balanced diet.")

    # Smoking
    if smoker == 1:
        suggestions.append("🚭 Smoking detected. Consider quitting to reduce health risks.")

    # Age based
    if age > 40:
        suggestions.append("🩺 Regular health checkups are recommended for your age group.")

    # Default healthy message
    if len(suggestions) == 0:
        suggestions.append("✅ You are maintaining a healthy lifestyle. Keep it up!")

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
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Inputs
        age = int(data["age"])
        income = float(data["income"])
        bmi = float(data["bmi"])
        smoker = int(data["smoker"])

        # Calculate risk
        risk_score = calculate_risk(age, income, bmi, smoker)

        # Get policies
        policies = recommend_policies(risk_score)

        # Basic suggestions
        suggestions = generate_suggestions(age, bmi, smoker)

        # 🔥 Smart AI Tips + Risk Level
        if risk_score < 30000:
            suggestions.append("🟢 Low Risk: Maintain your healthy lifestyle.")
            risk_level = "Low Risk"

        elif risk_score < 60000:
            suggestions.append("🟠 Medium Risk: Improve diet and increase physical activity.")
            risk_level = "Medium Risk"

        else:
            suggestions.append("🔴 High Risk: Consult a doctor and consider comprehensive insurance.")
            risk_level = "High Risk"

        # Response
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