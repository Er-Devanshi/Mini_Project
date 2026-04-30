from app import calculate_risk

def test_low_risk():
    result = calculate_risk(20, 20000, 20, 0)
    assert result < 30000

def test_high_risk_smoker():
    result = calculate_risk(50, 60000, 30, 1)
    assert result > 30000

def test_income_effect():
    low = calculate_risk(30, 20000, 25, 0)
    high = calculate_risk(30, 60000, 25, 0)
    assert high > low
    