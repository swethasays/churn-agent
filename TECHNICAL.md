# Churn Agent — Technical Decisions & Why

## The Problem I Was Solving

Customer churn prediction is a solved ML problem. Random Forest on Telco data is not novel.
The interesting problem I was solving was different:

> "How do you take a churn prediction model that sits in a notebook and turn it into something 
> a business can actually use — with explainability, automated actions, and human oversight?"

That is what this project is about. Not the ML. The system around the ML.

---

## Why LangGraph — not LangChain, not a simple script

Most people building AI projects use LangChain chains or just call the LLM directly.
I chose LangGraph specifically because my workflow had **conditional branching**.

```
predict → explain → analyze → [high_risk | medium_risk | low_risk] → report
```

A simple chain cannot do this. LangGraph gives you:
- **Nodes** — discrete steps with clear responsibility
- **Edges** — explicit flow between steps
- **Conditional edges** — route based on state (risk level)
- **State** — shared context that flows through the entire graph

If I had used a simple script, the routing logic would be buried in if/else blocks.
LangGraph makes the agent architecture **explicit and visible** — you can draw it as a graph
and it matches the code exactly. That matters for debugging and for explaining to teammates.

---

## Why SHAP — not just "the model said so"

The ML model gives a probability. That is not enough for a business user.

A customer success manager does not care that "the model scored 0.78".
They need to know: *"This customer is at risk because they are on a month-to-month contract,
have been with us for only 2 months, and their monthly charges are above average."*

SHAP (SHapley Additive exPlanations) gives exactly that — feature-level attribution.
For each prediction it tells you which features pushed the score up or down and by how much.

I used `shap.TreeExplainer` specifically because:
- It is optimised for tree-based models like Random Forest
- It is exact, not approximate
- It runs fast enough for real-time inference

The top 3 SHAP features per customer get passed to the LLM as context.
This means the LLM explanation is grounded in actual model reasoning — not hallucinated.

---

## Why Groq — not OpenAI

Two reasons:

1. **Speed** — Groq runs Llama 3.3-70b at ~500 tokens/second. For a dashboard where
   a user is waiting for results, latency matters. OpenAI GPT-4 is slower and more expensive.

2. **Cost** — Groq has a generous free tier. For a portfolio project that might get
   traffic from recruiters, I needed zero ongoing cost.

I used `llama-3.3-70b-versatile` specifically because it follows structured output
instructions reliably — critical when you need the LLM to return REASON, SUBJECT,
and EMAIL in a specific format that gets parsed downstream.

---

## Why Human-in-the-Loop — not fully automated

This was the most deliberate design decision.

The agent *could* send emails automatically. The SMTP code is there.
I chose not to because **AI should not take irreversible actions without human approval**.

Sending an email to a real customer is irreversible. If the LLM drafts something wrong —
a bad offer, wrong tone, incorrect information — you cannot unsend it.

The Human-in-the-Loop pattern means:
- Agent does the cognitive work — drafting, personalising, subject line
- Human does the judgment call — is this appropriate to send?
- Human can edit before sending — fixes any LLM errors
- Every decision is logged — audit trail for compliance

This is not a limitation of the system. It is a feature.
In production AI systems, human oversight on consequential actions is a requirement, not an afterthought.

---

## Why separate nodes for High/Medium/Low risk

I could have handled all risk levels in one node with if/else logic.
I gave each risk level its own node deliberately.

In a real system, these nodes would do very different things:
- **High risk** — trigger CRM update, alert sales team, send urgent email
- **Medium risk** — schedule follow-up call, add to nurture campaign
- **Low risk** — add to satisfaction survey queue, no immediate action

Separating them makes the system **extensible**. Adding a new action for High risk
customers means editing one node, not untangling shared logic.

This is the Open/Closed Principle applied to agent architecture.

---

## Why configurable thresholds — not hardcoded

The ML model outputs a probability. The business decides what that probability means.

A startup with high churn pressure might say "anyone above 50% is High Risk".
An enterprise with a large customer success team might say "only above 80%".

Hardcoding 0.7 as the High Risk threshold is a technical decision masquerading
as a business decision. I separated them — the model does math, the business sets policy.

The sliders in the Streamlit sidebar let a non-technical user change these thresholds
without touching any code. That is what configurability means in production.

---

## What I would do differently in v2

Being honest about limitations shows engineering maturity:

1. **Input validation with Pydantic** — currently no validation on the FastAPI endpoints.
   A bad payload would crash the agent rather than return a clean error.

2. **Rate limiting** — the Hugging Face deployment has no rate limiting.
   A malicious user could drain the Groq free tier in minutes by spamming requests.

3. **Output validation** — LLM output is parsed with string splitting.
   A more robust approach would use structured outputs or Pydantic to validate
   the LLM response before it enters the state.

4. **Model improvement** — Random Forest at 79% accuracy is a baseline.
   XGBoost or a calibrated probability model would give better results.
   More importantly, the model needs to be retrained on the company's own data,
   not Telco data, to be actually useful.

5. **LangSmith tracing** — integrated but disabled due to free tier limits.
   In production this would be essential for debugging agent behaviour.

---

## The real insight

The ML model is the least interesting part of this system.

The interesting engineering is the **pipeline around the model** —
how predictions become explanations, explanations become actions,
actions go through human review, and every decision gets logged.

That pipeline is what separates a data science notebook from a production AI system.