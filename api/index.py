from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class EmployeeInput(BaseModel):
    age: int
    monthly_income: float
    years_at_company: int
    months_at_company: int
    overtime: int           # 1 = Yes, 0 = No
    job_satisfaction: int   # 1 to 4
    work_life_balance: int  # 1 to 4

@app.post("/api/predict")
@app.post("/predict")
def predict_attrition(data: EmployeeInput):
    base_score = 0.15
    factors = []
    actions = []

    # Calculate total tenure in months
    total_months = (data.years_at_company * 12) + data.months_at_company

    # Logical Risk Scoring
    if data.overtime == 1:
        base_score += 0.25
        factors.append("High Overtime Frequency")
        actions.append("Audit workload distribution and enforce mandatory rest/comp-time to prevent burnout.")
        
    if data.job_satisfaction <= 2:
        base_score += 0.20
        factors.append("Low Job Satisfaction")
        actions.append("Schedule a 'stay interview' to identify blockers in their day-to-day role and map out career growth paths.")
        
    if data.work_life_balance <= 2:
        base_score += 0.15
        factors.append("Poor Work-Life Balance")
        actions.append("Offer flexible working hours, hybrid options, or a 4-day work week trial to improve baseline wellness.")
        
    # Adjusted for Indian Rupees (e.g., flagging below ₹30,000 as a risk factor depending on the role)
    if data.monthly_income < 30000:
        base_score += 0.15
        factors.append("Below-Average Salary Band")
        actions.append("Trigger an immediate compensation review against current market benchmarks for this role in India.")
        
    if total_months < 24:
        base_score += 0.10
        factors.append("Flight Risk: Low Tenure")
        actions.append("Increase check-ins and mentorship alignment to improve early-stage employee retention.")

    # Calculate final probability
    probability = min(max(base_score, 0.05), 0.95)
    is_high_risk = probability >= 0.45

    # Categorize Risk
    if probability > 0.60:
        risk_level = "CRITICAL"
        actions.insert(0, "🚨 URGENT: Flag to HR Business Partner for immediate retention intervention.")
    elif probability >= 0.45:
        risk_level = "WARNING"
    else:
        risk_level = "STABLE"
        actions = ["Continue current management approach. No immediate intervention required."]

    return {
        "attrition_risk": "High Risk" if is_high_risk else "Low Risk",
        "probability_percent": round(probability * 100, 1),
        "risk_level": risk_level,
        "key_risk_drivers": factors if factors else ["No critical risk drivers identified."],
        "recommended_actions": actions
    }
