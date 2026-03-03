def recommend_policy(risk_score):
    if risk_score < 30000:
        return "Basic Health Insurance Plan"
    elif risk_score < 60000:
        return "Standard Health Insurance Plan"
    else:
        return "Premium Comprehensive Plan"