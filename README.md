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

## What does it do?

Every business loses customers silently. This AI Agent helps you find them before they leave.

Give it a customer's data and it tells you:
- 🔴 **How likely** they are to leave (churn probability)
- 🔍 **Why** they are at risk (explained in plain English)
- 📧 **What to do** — personalized retention email drafted automatically
- 👤 **Human-in-the-Loop** — you review and approve before anything is sent

## How it works

```
Customer Data → ML Model → SHAP Explainer → LLM Email Writer → Human Approval → Send
```

1. Random Forest model scores churn probability
2. SHAP identifies top risk factors
3. Groq LLM drafts personalized retention email
4. Human reviews, edits, approves or rejects
5. Real email sent via Gmail SMTP

## 🛠️ Built With

| Tool | Purpose |
|------|---------|
| 🦜 LangGraph | AI agent framework |
| ⚡ Groq + Llama 3 | Fast LLM inference |
| 🌲 Scikit-learn | Random Forest churn model |
| 📊 SHAP | Explainability |
| 🚀 FastAPI | REST API |
| 🎨 Streamlit | Dashboard UI |
| 📧 Gmail SMTP | Real email sending |

## ✨ Key Features

- **Single customer analysis** — fill in details and get instant risk assessment
- **Batch CSV upload** — analyze your entire customer database at once
- **Configurable thresholds** — business users adjust risk levels without touching code
- **Human-in-the-Loop** — AI drafts, human decides
- **Audit trail** — approvals and rejections logged to CSV automatically

## 🚀 Run Locally

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

## 📁 Project Structure

```
churn-agent/
├── agent/
│   ├── graph.py        ← LangGraph agent graph
│   ├── nodes.py        ← all node logic
│   ├── state.py        ← agent state
│   └── tools.py        ← tools placeholder
├── ml/
│   ├── train.py        ← model training
│   └── predict.py      ← inference utilities
├── api/
│   └── main.py         ← FastAPI endpoints
├── models/
│   ├── churn_model.pkl
│   └── feature_names.pkl
├── app.py              ← Streamlit dashboard
├── Dockerfile
└── requirements.txt
```

## 👩‍💻 Built By

**Swetha Gatamaneni**  
[LinkedIn](https://linkedin.com/in/swetha-v-gatamaneni) · [GitHub](https://github.com/swethasays)
