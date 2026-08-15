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

    # 1. Overtime Impact
    if data.overtime == 1:
        base_score += 0.25
        factors.append("High Overtime Frequency & Workload Pressure")
        actions.append("Implement mandatory rest periods and redistribute project bandwidth to reduce burnout.")
    else:
        actions.append("Maintain standard operating hours and monitor ongoing sprint capacities.")

    # 2. Job Satisfaction Impact
    if data.job_satisfaction <= 2:
        base_score += 0.20
        factors.append("Low Job & Role Satisfaction")
        actions.append("Conduct a 1-on-1 Stay Interview to identify role blockers and realign daily tasks with career goals.")
    else:
        actions.append("Provide continuous upskilling pathways and cross-functional leadership opportunities.")

    # 3. Work-Life Balance Impact
    if data.work_life_balance <= 2:
        base_score += 0.15
        factors.append("Sub-optimal Work-Life Balance")
        actions.append("Introduce flexible working schedules or hybrid work flexibility to support baseline wellness.")
    else:
        actions.append("Sustain current team culture initiatives and wellness support programs.")

    # 4. Compensation Band (INR)
    if data.monthly_income < 30000:
        base_score += 0.15
        factors.append("Compensation Below Market Benchmark (Under ₹30k)")
        actions.append("Trigger an immediate compensation review against current industry salary bands.")

    # 5. Tenure Impact
    if total_months < 24:
        base_score += 0.10
        factors.append("Early Career/Tenure Flight Risk (< 2 Years)")

    # Calculate final probability percentage
    probability = min(max(base_score, 0.05), 0.95)
    is_high_risk = probability >= 0.45

    # Determine Risk Tier and Final Action Plan (Ensuring 3-4 curated points)
    if probability > 0.60:
        risk_level = "CRITICAL"
        actions.insert(0, "🚨 Immediate Intervention: Escalate retention risk to HR Business Partner within 48 hours.")
    elif probability >= 0.45:
        risk_level = "WARNING"
        actions.insert(0, "⚠️ Active Monitoring: Schedule monthly manager check-ins to track morale and sentiment.")
    else:
        risk_level = "STABLE"
        actions = [
            "Maintain current talent engagement cadence and quarterly performance reviews.",
            "Offer specialized technical certifications to encourage long-term retention.",
            "Recognize contributions in team forums to reinforce organizational loyalty.",
            "Review career trajectory periodically during annual appraisal cycles."
        ]

    # Trim to 4 key high-impact points maximum
    final_actions = actions[:4]

    return {
        "attrition_risk": "High Risk" if is_high_risk else "Low Risk",
        "probability_percent": round(probability * 100, 1),
        "risk_level": risk_level,
        "key_risk_drivers": factors if factors else ["No critical risk drivers identified. Employee profile indicates high stability."],
        "recommended_actions": final_actions
    }
