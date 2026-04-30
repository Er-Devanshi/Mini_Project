import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import calculate_risk

def test_basic():
    result = calculate_risk(30, 40000, 25, 0)
    assert result > 0

def test_smoker():
    non_smoker = calculate_risk(30, 40000, 25, 0)
    smoker = calculate_risk(30, 40000, 25, 1)
    assert smoker > non_smoker

def test_income_effect():
    low = calculate_risk(30, 20000, 25, 0)
    high = calculate_risk(30, 60000, 25, 0)
    assert high > low