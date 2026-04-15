import sys
import os
sys.path.insert(0, os.path.abspath("."))

from agent.graph import churn_agent

# ── Test Case 1: MEDIUM RISK ──────────────────────
test_customer = {
    "customer_id": "CUST-001",
    "customer_data": {
        "gender": 1,
        "SeniorCitizen": 0,
        "Partner": 1,
        "Dependents": 0,
        "tenure": 2,
        "PhoneService": 1,
        "MultipleLines": 0,
        "InternetService": 2,
        "OnlineSecurity": 0,
        "OnlineBackup": 0,
        "DeviceProtection": 0,
        "TechSupport": 0,
        "StreamingTV": 0,
        "StreamingMovies": 0,
        "Contract": 0,
        "PaperlessBilling": 1,
        "PaymentMethod": 2,
        "MonthlyCharges": 85.0,
        "TotalCharges": 170.0
    }
}

# ── Test Case 2: HIGH RISK ────────────────────────────────────
high_risk_customer = {
    "customer_id": "CUST-HIGH-001",
    "customer_data": {
        "gender": 1,
        "SeniorCitizen": 1,
        "Partner": 0,
        "Dependents": 0,
        "tenure": 1,
        "PhoneService": 1,
        "MultipleLines": 1,
        "InternetService": 2,
        "OnlineSecurity": 0,
        "OnlineBackup": 0,
        "DeviceProtection": 0,
        "TechSupport": 0,
        "StreamingTV": 1,
        "StreamingMovies": 1,
        "Contract": 0,
        "PaperlessBilling": 1,
        "PaymentMethod": 2,
        "MonthlyCharges": 105.0,
        "TotalCharges": 105.0
    }
}

# ── Test Case 3: LOW RISK ─────────────────────────────────────
low_risk_customer = {
    "customer_id": "CUST-LOW-003",
    "customer_data": {
        "gender": 0,
        "SeniorCitizen": 0,
        "Partner": 1,
        "Dependents": 1,
        "tenure": 60,
        "PhoneService": 1,
        "MultipleLines": 0,
        "InternetService": 1,
        "OnlineSecurity": 1,
        "OnlineBackup": 1,
        "DeviceProtection": 1,
        "TechSupport": 1,
        "StreamingTV": 0,
        "StreamingMovies": 0,
        "Contract": 2,
        "PaperlessBilling": 0,
        "PaymentMethod": 0,
        "MonthlyCharges": 45.0,
        "TotalCharges": 2700.0
    }
}

# ── Run all 3 ─────────────────────────────────────────────────
for customer in [test_customer, high_risk_customer, low_risk_customer]:
    result = churn_agent.invoke(customer)
    print(result["report"])

# ── Show graph ────────────────────────────────────────────────
print(churn_agent.get_graph().draw_ascii())