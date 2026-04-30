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

    # ✅ FIXED Income Logic
    if income > 50000:
        income_score = 15000
    elif income > 30000:
        income_score = 8000
    else:
        income_score = 2000

    risk += income_score
    breakdown["income"] = income_score

    return risk, breakdown