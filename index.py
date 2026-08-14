from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class EmployeeInput(BaseModel):
    age: int
    monthly_income: float
    years_at_company: int
    overtime: int           # 1 = Yes, 0 = No
    job_satisfaction: int   # 1 to 4
    work_life_balance: int  # 1 to 4

@app.post("/api/predict")
def predict_attrition(data: EmployeeInput):
    # Risk scoring algorithm simulating ML classification
    base_score = 0.15

    if data.overtime == 1:
        base_score += 0.25
    if data.job_satisfaction <= 2:
        base_score += 0.20
    if data.work_life_balance <= 2:
        base_score += 0.15
    if data.monthly_income < 3500:
        base_score += 0.15
    if data.years_at_company < 2:
        base_score += 0.10

    probability = min(max(base_score, 0.05), 0.95)
    is_high_risk = probability >= 0.45

    factors = []
    if data.overtime == 1:
        factors.append("High Overtime Frequency")
    if data.job_satisfaction <= 2:
        factors.append("Low Job Satisfaction")
    if data.work_life_balance <= 2:
        factors.append("Poor Work-Life Balance")
    if data.monthly_income < 3500:
        factors.append("Below-Average Salary Band")

    return {
        "attrition_risk": "High Risk" if is_high_risk else "Low Risk",
        "probability_percent": round(probability * 100, 1),
        "risk_level": "CRITICAL" if probability > 0.60 else ("WARNING" if probability >= 0.45 else "STABLE"),
        "key_risk_drivers": factors if factors else ["No critical risk drivers identified."]
    }