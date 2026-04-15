import joblib
import shap
import numpy as np
import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Load model once
model         = joblib.load("models/churn_model.pkl")
feature_names = joblib.load("models/feature_names.pkl")
explainer     = shap.TreeExplainer(model)

# Load LLM once
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# ── Node 1: Validate ─────────────────────────────────────────
def validate_data(state: dict) -> dict:
    data    = state["customer_data"]
    missing = [f for f in feature_names if f not in data]
    if missing:
        raise ValueError(f"Missing features: {missing}")
    print(f"✅ Data validated for {state['customer_id']}")
    return state

# ── Node 2: Predict ──────────────────────────────────────────
def predict_churn(state: dict) -> dict:
    data = state["customer_data"]
    df   = pd.DataFrame([data])[feature_names]
    prob = model.predict_proba(df)[0][1]

    # Use thresholds from state not hardcoded
    high_threshold   = state.get("high_threshold",   0.7)
    medium_threshold = state.get("medium_threshold", 0.4)

    if prob >= high_threshold:
        risk = "High"
    elif prob >= medium_threshold:
        risk = "Medium"
    else:
        risk = "Low"

    print(f"🔮 Probability: {prob:.2f} → Risk: {risk}")
    return {**state, "churn_probability": round(float(prob), 4), "risk_level": risk}

# ── Node 3: Explain with SHAP ────────────────────────────────
def explain_churn(state: dict) -> dict:
    data        = state["customer_data"]
    df          = pd.DataFrame([data])[feature_names]
    shap_values = explainer(df)

    vals     = shap_values.values[0][:, 1]
    top_idx  = np.argsort(np.abs(vals))[::-1][:3]
    top_features = [
        f"{feature_names[i]}: {data[feature_names[i]]} (impact: {vals[i]:+.3f})"
        for i in top_idx
    ]

    reason = " | ".join(top_features)
    print(f"🔍 SHAP: {reason}")
    return {**state, "churn_reason": reason}

# ── Node 4: LLM analysis ─────────────────────────────────────
def analyze_and_respond(state: dict) -> dict:
    prompt = f"""
You are a customer retention specialist.

Customer risk level: {state['risk_level']}
Churn probability: {state['churn_probability']}
Key risk factors: {state['churn_reason']}

Do two things:
1. In 2 sentences explain in plain English why this customer is at risk.
2. Write a short personalized retention email (max 5 sentences).

Format exactly like this:
REASON: <your explanation>
SUBJECT: <short compelling subject line>
EMAIL:
Dear Customer,

[opening sentence]

[middle sentence with offer]

[closing sentence]

Best regards,
Customer Success Team
"""
    response    = llm.invoke([HumanMessage(content=prompt)])
    text        = response.content
    reason_line  = [l for l in text.split("\n") if l.startswith("REASON:")]
    subject_line = [l for l in text.split("\n") if l.startswith("SUBJECT:")]
    email_line   = [l for l in text.split("\n") if l.startswith("EMAIL:")]

    reason  = reason_line[0].replace("REASON:", "").strip()   if reason_line  else text
    subject = subject_line[0].replace("SUBJECT:", "").strip() if subject_line else "We value your business"

    # Get everything after EMAIL: line
    if email_line:
        email_start = text.find("EMAIL:")
        email = text[email_start:].replace("EMAIL:", "").strip()
    else:
        email = ""

    full_email = f"Subject: {subject}\n\n{email}"

    print(f"🤖 LLM done")
    return {**state, "churn_reason": reason, "retention_message": full_email}

# ── Node 5: Router ───────────────────────────────────────────
def route_by_risk(state: dict) -> str:
    risk = state["risk_level"]
    print(f"🔀 Routing: {risk}")
    if risk == "High":
        return "high_risk"
    elif risk == "Medium":
        return "medium_risk"
    else:
        return "low_risk"

# ── Node 6a: High risk ───────────────────────────────────────
def handle_high_risk(state: dict) -> dict:
    action = "URGENT: Send retention email + 20% discount offer"
    print(f"🚨 {action}")
    return {**state, "action_taken": action}

# ── Node 6b: Medium risk ─────────────────────────────────────
def handle_medium_risk(state: dict) -> dict:
    action = "Schedule follow-up call + offer loyalty reward"
    print(f"⚠️  {action}")
    return {**state, "action_taken": action}

# ── Node 6c: Low risk ────────────────────────────────────────
def handle_low_risk(state: dict) -> dict:
    action = "Monitor for 30 days + send satisfaction survey"
    print(f"✅ {action}")
    return {**state, "action_taken": action}

# ── Node 7: Report ───────────────────────────────────────────
def generate_report(state: dict) -> dict:
    report = f"""
=== CHURN AGENT REPORT ===
Customer ID : {state['customer_id']}
Risk Level  : {state['risk_level']}
Churn Prob  : {state['churn_probability']*100:.1f}%
Why At Risk : {state['churn_reason']}
Action      : {state['action_taken']}
Email Draft : {state['retention_message']}
==========================
"""
    # removed print here — dashboard will display it
    return {**state, "report": report}