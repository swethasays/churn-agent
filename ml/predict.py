# predict.py
# ─────────────────────────────────────────────
# This file is reserved for standalone
# inference logic — running predictions
# outside of the LangGraph agent.
#
# Current implementation runs predictions
# inside the agent pipeline (see agent/nodes.py)
# via the predict_churn() node.
#
# Planned for v2:
# - batch_predict(df) → predict entire DataFrame
# - predict_single(customer_dict) → single prediction
# - load_model() → model loading utility
# ─────────────────────────────────────────────

import joblib
import pandas as pd

# Load model and feature names
model         = joblib.load("models/churn_model.pkl")
feature_names = joblib.load("models/feature_names.pkl")

def predict_single(customer_data: dict) -> dict:
    """
    Run churn prediction on a single customer.
    Returns probability and risk level.
    """
    df   = pd.DataFrame([customer_data])[feature_names]
    prob = model.predict_proba(df)[0][1]

    if prob >= 0.7:
        risk = "High"
    elif prob >= 0.4:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "churn_probability": round(float(prob), 4),
        "risk_level":        risk
    }

def batch_predict(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run churn prediction on an entire DataFrame.
    Returns DataFrame with probability and risk columns added.
    """
    X     = df[feature_names]
    probs = model.predict_proba(X)[:, 1]

    df = df.copy()
    df["churn_probability"] = probs.round(4)
    df["risk_level"] = df["churn_probability"].apply(
        lambda p: "High" if p >= 0.7 else "Medium" if p >= 0.4 else "Low"
    )

    return df