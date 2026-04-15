from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

sys.path.insert(0, os.path.abspath("."))

from agent.graph import churn_agent

app = FastAPI(
    title="Churn Agent API",
    description="Production LangGraph AI Agent for customer churn prediction",
    version="1.0.0"
)

# ── Request model ─────────────────────────────────────────────
class CustomerRequest(BaseModel):
    customer_id:   str
    customer_data: dict

# ── Response model ────────────────────────────────────────────
class AgentResponse(BaseModel):
    customer_id:       str
    risk_level:        str
    churn_probability: float
    churn_reason:      str
    action_taken:      str
    retention_message: str
    report:            str

# ── Health check ──────────────────────────────────────────────
@app.get("/")
def health_check():
    return {
        "status":  "running",
        "agent":   "churn-agent",
        "version": "1.0.0"
    }

# ── Single prediction ─────────────────────────────────────────
@app.post("/predict", response_model=AgentResponse)
def predict(request: CustomerRequest):
    try:
        result = churn_agent.invoke({
            "customer_id":   request.customer_id,
            "customer_data": request.customer_data
        })
        return AgentResponse(
            customer_id       = result["customer_id"],
            risk_level        = result["risk_level"],
            churn_probability = result["churn_probability"],
            churn_reason      = result["churn_reason"],
            action_taken      = result["action_taken"],
            retention_message = result["retention_message"],
            report            = result["report"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Batch prediction ──────────────────────────────────────────
@app.post("/predict/batch")
def predict_batch(requests: list[CustomerRequest]):
    results = []
    for req in requests:
        try:
            result = churn_agent.invoke({
                "customer_id":   req.customer_id,
                "customer_data": req.customer_data
            })
            results.append({
                "customer_id":       result["customer_id"],
                "risk_level":        result["risk_level"],
                "churn_probability": result["churn_probability"],
                "action_taken":      result["action_taken"]
            })
        except Exception as e:
            results.append({
                "customer_id": req.customer_id,
                "error":       str(e)
            })
    return {"results": results, "total": len(results)}