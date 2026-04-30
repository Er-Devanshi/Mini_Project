from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# -------------------------------
# Risk Calculation
# -------------------------------
def calculate_risk(age, income, bmi, smoker):
    risk = 0
    breakdown = {}

    # Age
    age_score = age * 80
    risk += age_score
    breakdown["age"] = age_score

    # BMI
    bmi_score = bmi * 150
    risk += bmi_score
    breakdown["bmi"] = bmi_score

    # Smoking
    smoker_score = 20000 if smoker == 1 else 0
    risk += smoker_score
    breakdown["smoker"] = smoker_score

    # ✅ FIXED Income Logic (important for tests)
    if income > 50000:
        income_score = 15000
    elif income > 30000:
        income_score = 8000
    else:
        income_score = 2000

    risk += income_score
    breakdown["income"] = income_score

    return risk, breakdown


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
        suggestions.append("⚠️ Your BMI is high. Try exercise and diet.")

    if smoker == 1:
        suggestions.append("🚭 Consider quitting smoking.")

    if age > 40:
        suggestions.append("🩺 Regular health checkups recommended.")

    if not suggestions:
        suggestions.append("✅ Healthy lifestyle. Keep it up!")

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

        age = int(data["age"])
        income = float(data["income"])
        bmi = float(data["bmi"])
        smoker = int(data["smoker"])

        risk_score, breakdown = calculate_risk(age, income, bmi, smoker)

        policies = recommend_policies(risk_score)
        suggestions = generate_suggestions(age, bmi, smoker)

        # Risk Level
        if risk_score < 30000:
            risk_level = "Low Risk"
        elif risk_score < 60000:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

        return jsonify({
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommended_policy": policies[0],
            "all_policies": policies,
            "suggestions": suggestions,
            "breakdown": breakdown
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# -------------------------------
# Run App (IMPORTANT FIX)
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)