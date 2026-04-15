---
title: Churn Agent
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# 🤖 Churn Agent — AI-Powered Customer Retention

> Predict who is leaving, understand why, and act before it's too late.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-green)
![Groq](https://img.shields.io/badge/Groq-Llama3.3-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-deployed-red)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)

### 🔴 [Live Demo → huggingface.co/spaces/swethasays/churn-agent](https://huggingface.co/spaces/swethasays/churn-agent)

---

## What this does

A customer success manager enters a customer's profile. The system instantly returns:

- **Churn probability** with a risk tier — Low / Medium / High
- **Top 3 risk drivers** powered by SHAP explainability in plain English
- **A personalized retention email** drafted by Llama 3.3 70B via Groq
- **Human-in-the-Loop approval** — review, edit, approve or reject before anything is sent
- **Real email delivery** via Gmail SMTP with full audit trail

---

## Why it is different

Most churn projects stop at model accuracy. This one builds the full production system:

| What others do | What this does |
|---|---|
| Train a model, print accuracy | Full pipeline from data to live deployed agent |
| Black-box predictions | SHAP explains every single prediction |
| No deployment | Live app anyone can use right now |
| Generic output | LLM writes personalized retention email per customer |
| Fully automated | Human-in-the-Loop — agent suggests, human decides |
| No audit trail | Every approval and rejection logged to CSV |

---

## Results

| Metric | Value |
|---|---|
| Random Forest ROC-AUC | **0.84** |
| Training samples | 5,634 |
| Test samples | 1,409 |
| Churn rate in dataset | 26.5% |
| Dataset | Telco Customer Churn (Kaggle) |

Top predictors identified by SHAP: contract type, tenure, and monthly charges —
consistent with real-world telecom churn research.

---

## How it works

```
Customer Data → Validate → Predict → SHAP Explain → LLM Draft Email
                                                            ↓
                                              [High / Medium / Low Risk Node]
                                                            ↓
                                              Human Reviews → Approve → Send
                                                          → Reject → Log
```

1. **Validate** — check all required features are present
2. **Predict** — Random Forest scores churn probability
3. **Explain** — SHAP identifies top 3 risk factors per customer
4. **Analyze** — Groq LLM drafts personalized retention email
5. **Route** — LangGraph routes to High, Medium, or Low risk node
6. **Report** — full agent report generated
7. **Human decision** — approve and send real email, or reject and log

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data & Modelling | Python, Pandas, Scikit-learn |
| Explainability | SHAP (TreeExplainer) |
| Agent Framework | LangGraph |
| LLM | Groq + Llama 3.3 70B |
| API | FastAPI, Uvicorn |
| Dashboard | Streamlit |
| Email | Gmail SMTP |
| Deployment | Docker, Hugging Face Spaces |

---

## Key Decisions

**Why LangGraph over a simple script?**
The workflow has conditional branching — High, Medium, and Low risk customers need
different actions. LangGraph makes this routing explicit and visible as a graph.
A simple script would bury this logic in if/else blocks that are hard to extend.

**Why SHAP?**
The ML model gives a probability. That is not enough for a business user.
TreeSHAP gives feature-level attribution per prediction — so the LLM explanation
is grounded in actual model reasoning, not hallucinated.

**Why Groq?**
~500 tokens/second on Llama 3.3 70B makes real-time email drafting practical.
For a dashboard where a user is waiting for results, latency matters.

**Why Human-in-the-Loop?**
Sending an email to a real customer is irreversible. If the LLM drafts something
wrong, you cannot unsend it. The agent drafts, the human decides. This is not a
limitation — it is a deliberate production safety pattern.

**Why configurable thresholds?**
Hardcoding 0.7 as High Risk is a technical decision masquerading as a business decision.
Business users can adjust thresholds via sliders without touching any code.

---

## If this were production

- **Input validation** — Pydantic validation on FastAPI endpoints
- **Rate limiting** — prevent API abuse and Groq free tier exhaustion
- **Model retraining** — scheduled pipeline on fresh customer data
- **LangSmith tracing** — agent monitoring and trace visualization (integrated, disabled due to free tier)
- **Database logging** — PostgreSQL instead of CSV for audit trail
- **Auth** — JWT authentication before exposing API to users
- **CI/CD** — GitHub Actions for automated testing and deployment

---

## Run Locally

```bash
git clone https://github.com/swethasays/churn-agent
cd churn-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your keys to `.env`:

```
GROQ_API_KEY=your_key
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
LANGCHAIN_TRACING_V2=false
```

Train the model:

```bash
python ml/train.py
```

Run the app:

```bash
streamlit run app.py
```

---

## Project Structure

```
churn-agent/
├── agent/
│   ├── graph.py        ← LangGraph agent graph
│   ├── nodes.py        ← all node logic
│   ├── state.py        ← agent state
│   └── tools.py        ← tools placeholder (v2)
├── ml/
│   ├── train.py        ← model training
│   └── predict.py      ← inference utilities
├── api/
│   └── main.py         ← FastAPI endpoints
├── models/
│   ├── churn_model.pkl
│   └── feature_names.pkl
├── app.py              ← Streamlit dashboard
├── TECHNICAL.md        ← architecture and design decisions
├── Dockerfile
└── requirements.txt
```

---

## STAR Summary

**Situation**
A telecom company loses customers silently — by the time they notice churn,
it is too late to act. Existing tools predict churn but do not tell teams what to do about it.

**Task**
Build an end-to-end AI agent that predicts churn, explains the reasons,
drafts a personalized retention email, and sends it — with human oversight throughout.

**Action**
Trained a Random Forest classifier with SHAP explainability, designed a multi-node
LangGraph agent with conditional risk routing, integrated Groq LLM for email generation,
built a human-in-the-loop approval flow with real Gmail SMTP delivery and CSV audit logging,
deployed via Docker on Hugging Face Spaces with a Streamlit dashboard.

**Result**
ROC-AUC of 0.84, live deployable agent with real email delivery, configurable risk thresholds
for business users, and a full audit trail of every human decision — accessible to anyone via live demo.

---

## Dataset

[Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) —
7,043 customer records, 20 features, binary churn label. 26.5% churn rate.

---

## 👩‍💻 Built By

**Swetha Gatamaneni**
[LinkedIn](https://linkedin.com/in/swetha-v-gatamaneni) · [GitHub](https://github.com/swethasays)