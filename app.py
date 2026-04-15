import streamlit as st
import pandas as pd
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.insert(0, os.path.abspath("."))
from agent.graph import churn_agent

def send_email(to_address: str, subject: str, body: str) -> bool:
    try:
        sender   = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        msg = MIMEMultipart()
        msg["From"]    = sender
        msg["To"]      = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, to_address, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Churn Agent",
    page_icon="🤖",
    layout="wide"
)

# ── Sidebar FIRST (thresholds needed before everything) ───────
st.sidebar.title("⚙️ Settings")

st.sidebar.markdown("""
### What are Risk Thresholds?
These sliders let **business users** control 
when a customer is flagged as High, Medium, 
or Low risk — without touching any code.

**Real world example:**
A telecom manager says:
> *"We want to be more aggressive. Flag anyone 
> above 50% as High Risk, not 70%."*

They just move the slider. Done.
No developer needed.

This is called **configurability** — a key 
sign of a production-ready system.
""")

st.sidebar.divider()
st.sidebar.markdown("### Adjust Thresholds")

high_threshold = st.sidebar.slider(
    "🚨 High Risk above",
    min_value=0.1,
    max_value=1.0,
    value=0.7,
    step=0.05,
    help="Customers above this probability are High Risk"
)

medium_threshold = st.sidebar.slider(
    "⚠️ Medium Risk above",
    min_value=0.1,
    max_value=float(round(high_threshold - 0.05, 2)),
    value=min(0.4, float(round(high_threshold - 0.05, 2))),
    step=0.05,
    help="Automatically stays below High Risk threshold — adjusts if you move the High Risk slider"
)

st.sidebar.success(f"""
✅ Current thresholds

🚨 High Risk   → above {high_threshold:.0%}
⚠️ Medium Risk → {medium_threshold:.0%} to {high_threshold:.0%}
✅ Low Risk    → below {medium_threshold:.0%}
""")

st.sidebar.divider()
st.sidebar.markdown("""
### About this project
Built with:
- 🦜 **LangGraph** — AI agent framework
- ⚡ **Groq** — fast LLM inference
- 🌲 **Scikit-learn** — ML model
- 📊 **SHAP** — explainability
- 🚀 **FastAPI** — production API
""")

# ── Header ────────────────────────────────────────────────────
st.title("🤖 Churn Agent Dashboard")
st.markdown("##### *Predict who is leaving, understand why, and act before it's too late.*")

st.markdown("""
Every business loses customers silently. This AI Agent helps you **find them before they leave** — 
and tells you exactly what to do about it.
""")

st.markdown("### How does it work?")
st.markdown("""
<div style="display: flex; gap: 12px; margin-bottom: 1rem;">
  <div style="flex:1; background:#e8f4fd; border-radius:8px; padding:16px; text-align:center; min-height:100px;">
    <div style="font-size:1.4em;">📋</div>
    <div style="font-weight:bold; margin:6px 0;">Step 1</div>
    <div style="font-size:0.9em;">Enter customer data</div>
  </div>
  <div style="flex:1; background:#e8f4fd; border-radius:8px; padding:16px; text-align:center; min-height:100px;">
    <div style="font-size:1.4em;">🤖</div>
    <div style="font-weight:bold; margin:6px 0;">Step 2</div>
    <div style="font-size:0.9em;">ML model scores churn risk</div>
  </div>
  <div style="flex:1; background:#e8f4fd; border-radius:8px; padding:16px; text-align:center; min-height:100px;">
    <div style="font-size:1.4em;">📊</div>
    <div style="font-weight:bold; margin:6px 0;">Step 3</div>
    <div style="font-size:0.9em;">SHAP explains the why</div>
  </div>
  <div style="flex:1; background:#e8f4fd; border-radius:8px; padding:16px; text-align:center; min-height:100px;">
    <div style="font-size:1.4em;">✉️</div>
    <div style="font-weight:bold; margin:6px 0;">Step 4</div>
    <div style="font-size:0.9em;">AI drafts retention email</div>
  </div>
  <div style="flex:1; background:#e8f4fd; border-radius:8px; padding:16px; text-align:center; min-height:100px;">
    <div style="font-size:1.4em;">📋</div>
    <div style="font-weight:bold; margin:6px 0;">Step 5</div>
    <div style="font-size:0.9em;">You get a full report</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["👤 Single Customer", "📂 Batch CSV Upload"])

# ════════════════════════════════════════════════════════════════
# TAB 1 — Single Customer
# ════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Analyze a Single Customer")
    st.markdown("""
    Fill in the customer details below and click **Run Churn Agent**.
    The agent will analyze the data and give you everything you need.

    > 💡 **Try this:** The form is already pre-filled with a sample customer — 
    > just click **Run Churn Agent** to see the agent in action.
    """)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**👤 Customer Info**")
        customer_id = st.text_input("Customer ID", "CUST-001")
        gender      = st.selectbox("Gender", [0, 1],
                        format_func=lambda x: "Female" if x == 0 else "Male")
        senior      = st.selectbox("Senior Citizen", [0, 1],
                        format_func=lambda x: "No" if x == 0 else "Yes")
        partner     = st.selectbox("Partner", [0, 1],
                        format_func=lambda x: "No" if x == 0 else "Yes")
        dependents  = st.selectbox("Dependents", [0, 1],
                        format_func=lambda x: "No" if x == 0 else "Yes")
        tenure      = st.slider("Tenure (months)", 0, 72, 2,
                        help="How long has this customer been with you?")

    with col2:
        st.markdown("**📡 Services**")
        phone          = st.selectbox("Phone Service", [0, 1],
                            format_func=lambda x: "No" if x == 0 else "Yes")
        multiple_lines = st.selectbox("Multiple Lines", [0, 1],
                            format_func=lambda x: "No" if x == 0 else "Yes")
        internet       = st.selectbox("Internet Service", [0, 1, 2],
                            format_func=lambda x: ["No", "DSL", "Fiber"][x])
        security       = st.selectbox("Online Security", [0, 1],
                            format_func=lambda x: "No" if x == 0 else "Yes")
        backup         = st.selectbox("Online Backup", [0, 1],
                            format_func=lambda x: "No" if x == 0 else "Yes")
        device         = st.selectbox("Device Protection", [0, 1],
                            format_func=lambda x: "No" if x == 0 else "Yes")
        tech_support   = st.selectbox("Tech Support", [0, 1],
                            format_func=lambda x: "No" if x == 0 else "Yes")
        tv             = st.selectbox("Streaming TV", [0, 1],
                            format_func=lambda x: "No" if x == 0 else "Yes")
        movies         = st.selectbox("Streaming Movies", [0, 1],
                            format_func=lambda x: "No" if x == 0 else "Yes")

    with col3:
        st.markdown("**💳 Contract & Billing**")
        contract  = st.selectbox("Contract Type", [0, 1, 2],
                        format_func=lambda x: ["Month-to-month", "One year", "Two year"][x],
                        help="Month-to-month customers churn 3x more")
        paperless = st.selectbox("Paperless Billing", [0, 1],
                        format_func=lambda x: "No" if x == 0 else "Yes")
        payment   = st.selectbox("Payment Method", [0, 1, 2, 3],
                        format_func=lambda x: ["Bank transfer", "Credit card",
                                               "Electronic check", "Mailed check"][x])
        monthly   = st.number_input("Monthly Charges ($)", 0.0, 200.0, 85.0,
                        help="Higher charges = higher churn risk")
        total     = st.number_input("Total Charges ($)", 0.0, 10000.0, 170.0)

    st.divider()

    if st.button("🚀 Run Churn Agent", type="primary", use_container_width=True):
        with st.spinner("🤖 Agent is thinking..."):
            customer_data = {
                "gender": gender, "SeniorCitizen": senior,
                "Partner": partner, "Dependents": dependents,
                "tenure": tenure, "PhoneService": phone,
                "MultipleLines": multiple_lines, "InternetService": internet,
                "OnlineSecurity": security, "OnlineBackup": backup,
                "DeviceProtection": device, "TechSupport": tech_support,
                "StreamingTV": tv, "StreamingMovies": movies,
                "Contract": contract, "PaperlessBilling": paperless,
                "PaymentMethod": payment, "MonthlyCharges": monthly,
                "TotalCharges": total
            }
            st.session_state.result      = churn_agent.invoke({
                "customer_id":      customer_id,
                "customer_data":    customer_data,
                "high_threshold":   high_threshold,
                "medium_threshold": medium_threshold
            })
            st.session_state.customer_id = customer_id

    # ── Results — shown OUTSIDE button block ──────────────────
    if "result" in st.session_state:
        result      = st.session_state.result
        customer_id = st.session_state.customer_id
        prob        = result["churn_probability"]
        risk        = result["risk_level"]
        action      = result["action_taken"]
        prob_display = prob * 100

        st.divider()
        st.markdown("## 📊 Agent Results")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if risk == "High":
                st.error(f"🚨 Risk Level: **{risk}**")
            elif risk == "Medium":
                st.warning(f"⚠️ Risk Level: **{risk}**")
            else:
                st.success(f"✅ Risk Level: **{risk}**")
        with col_b:
            st.metric("Churn Probability", f"{prob_display:.1f}%")
        with col_c:
            st.metric("Risk Protocol", f"{risk} Risk")

        st.divider()
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("### 🔍 Why is this customer at risk?")
            st.markdown("> *Explained by AI using SHAP values.*")
            st.info(result["churn_reason"])
        with col_right:
            st.markdown("### 📧 Retention Email — Ready to Send")
            st.markdown("> *Drafted automatically by the AI agent.*")
            st.success(result["retention_message"])

        st.divider()
        st.markdown("### ⚡ Action Taken by Agent")
        if risk == "High":
            st.error(f"🚨 {action}")
        elif risk == "Medium":
            st.warning(f"⚠️ {action}")
        else:
            st.success(f"✅ {action}")

        # ── Human in the Loop ─────────────────────────────────
        st.divider()
        st.markdown("### 👤 Human-in-the-Loop")
        st.markdown("""
        > *Production pattern — the agent drafts the email, 
        > a human reviews and approves before anything is sent.*
        """)

        email_parts   = result["retention_message"].split("\n\n", 1)
        email_subject = email_parts[0].replace("Subject:", "").strip() if len(email_parts) > 1 else "We value your business"
        email_body    = email_parts[1].strip() if len(email_parts) > 1 else result["retention_message"]

        st.markdown("**📧 Review and edit before sending — the AI drafted this, but you have the final say.**")
        edited_subject = st.text_input("Subject line", value=email_subject)
        edited_body    = st.text_area("Email body", value=email_body, height=200)

        col_a, col_b = st.columns(2)
        with col_a:
            recipient = st.text_input("📧 Send to email address", placeholder="customer@example.com")
            if st.button("✅ Approve & Send", type="primary", use_container_width=True):
                if recipient:
                    sent = send_email(recipient, edited_subject, edited_body)
                    if sent:
                        import csv
                        from datetime import datetime

                        log_row = {
                            "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "customer_id": customer_id,
                            "risk_level":  risk,
                            "churn_prob":  f"{prob_display:.1f}%",
                            "recipient":   recipient,
                            "subject":     edited_subject,
                            "action":      "Retention email approved and sent"
                        }

                        log_file = "approvals.csv"
                        file_exists = os.path.exists(log_file)

                        with open(log_file, "a", newline="") as f:
                            writer = csv.DictWriter(f, fieldnames=log_row.keys())
                            if not file_exists:
                                writer.writeheader()
                            writer.writerow(log_row)

                        st.success(f"""
                        ✅ Email sent to **{recipient}**!
                        - ✉️ Email delivered
                        - 👤 Customer: {customer_id}
                        - 🎯 Risk: {risk}
                        - 🕐 Time: {log_row['timestamp']}
                        - 📋 Saved to approvals.csv
                        """)
                else:
                    st.error("Please enter a recipient email address.")

        with col_b:
            if st.button("❌ Reject", use_container_width=True):
                import csv
                from datetime import datetime

                log_row = {
                    "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "customer_id": customer_id,
                    "risk_level":  risk,
                    "churn_prob":  f"{prob_display:.1f}%",
                    "action":      "Email rejected by human reviewer"
                }

                log_file = "rejections.csv"
                file_exists = os.path.exists(log_file)

                with open(log_file, "a", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=log_row.keys())
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(log_row)

                st.warning(f"""
                ❌ Rejected and logged.
                - 👤 Customer: {customer_id}
                - 🎯 Risk: {risk}
                - 🕐 Time: {log_row['timestamp']}
                - 📋 Saved to rejections.csv
                """)

        with st.expander("📋 View Full Agent Report"):
            st.code(result["report"])

# ════════════════════════════════════════════════════════════════
# TAB 2 — Batch CSV
# ════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Analyze Multiple Customers via CSV")
    st.markdown("""
    Instead of checking customers one by one, upload your entire customer database and instantly see **who is about to leave, why, and what action to take** — at scale.

    > 💡 **Test it:** Use the [Telco Churn dataset from Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) — works out of the box.
    """)

    st.warning("""
    ⚠️ **Rate limit note:** Each customer = 1 LLM call. 
    For large files (500+ rows) this will take several minutes. 
    Start with a small sample to test first.
    """)

    uploaded_file = st.file_uploader(
        "📂 Upload your CSV file here",
        type="csv"
    )

    if uploaded_file:
        from sklearn.preprocessing import LabelEncoder
        import joblib

        df = pd.read_csv(uploaded_file)
        feature_names = joblib.load("models/feature_names.pkl")

        # Auto encode text columns to numbers
        df_encoded = df.copy()
        le = LabelEncoder()
        for col in df_encoded.select_dtypes(include=["object"]).columns:
            if col != "customerID":
                df_encoded[col] = le.fit_transform(
                    df_encoded[col].astype(str)
                )

        # Fix TotalCharges blanks
        df_encoded["TotalCharges"] = pd.to_numeric(
            df_encoded["TotalCharges"], errors="coerce"
        ).fillna(0)

        st.write(f"✅ Loaded **{len(df)} customers**")
        st.dataframe(df.head())  # show original readable data

        if st.button("🚀 Run Agent on All Customers", type="primary"):
            results  = []
            progress = st.progress(0)
            status   = st.empty()

            for i, row in df_encoded.iterrows():
                status.text(f"Analyzing customer {i+1} of {len(df)}...")
                try:
                    # Only pass feature columns the model knows
                    customer_data = {
                        col: row[col]
                        for col in feature_names
                        if col in row
                    }

                    result = churn_agent.invoke({
                        "customer_id":      str(df.iloc[i].get("customerID", f"CUST-{i}")),
                        "customer_data":    customer_data,
                        "high_threshold":   high_threshold,
                        "medium_threshold": medium_threshold
                    })
                    results.append({
                        "Customer ID":  result["customer_id"],
                        "Risk Level":   result["risk_level"],
                        "Churn Prob %": f"{result['churn_probability']*100:.1f}%",
                        "Action":       result["action_taken"]
                    })
                except Exception as e:
                    results.append({
                        "Customer ID":  str(df.iloc[i].get("customerID", f"CUST-{i}")),
                        "Risk Level":   "Error",
                        "Churn Prob %": "N/A",
                        "Action":       str(e)
                    })
                progress.progress((i + 1) / len(df))

            status.text("Done!")
            results_df = pd.DataFrame(results)

            st.divider()
            st.markdown("### 📊 Summary")

            high   = len(results_df[results_df["Risk Level"] == "High"])
            medium = len(results_df[results_df["Risk Level"] == "Medium"])
            low    = len(results_df[results_df["Risk Level"] == "Low"])

            c1, c2, c3 = st.columns(3)
            c1.metric("🚨 High Risk Customers",   high)
            c2.metric("⚠️ Medium Risk Customers", medium)
            c3.metric("✅ Low Risk Customers",    low)

            st.divider()
            st.markdown("### Full Results Table")
            st.dataframe(results_df, use_container_width=True)


# ── FAQ ───────────────────────────────────────────────────────
st.divider()
st.markdown("### 🙋 Not sure about something?")

with st.expander("What is churn and why does it matter?"):
    st.markdown("""
    **Churn** means a customer stops using your service and leaves.
    
    Acquiring a new customer costs 5-7x more than retaining an existing one. 
    That's why catching customers *before* they leave is so valuable — 
    even saving 10% of at-risk customers can significantly impact revenue.
    """)

with st.expander("How does the AI know who will leave?"):
    st.markdown("""
    The AI was trained on thousands of real customer records. It learned 
    patterns — like customers on month-to-month contracts with high bills 
    and short tenure tend to leave more often.
    
    When you enter a customer's data, it compares them against those patterns 
    and gives a probability score from 0% to 100%.
    """)

with st.expander("What does the risk level mean?"):
    st.markdown("""
    - 🚨 **High Risk** — Customer is very likely to leave. Act immediately.
    - ⚠️ **Medium Risk** — Customer shows warning signs. Follow up soon.
    - ✅ **Low Risk** — Customer appears satisfied. Monitor periodically.
    
    You can adjust these thresholds from the sidebar based on your business needs.
    """)

with st.expander("What is SHAP and why does it say certain factors matter?"):
    st.markdown("""
    SHAP is a technique that explains *why* the AI made a decision — not just what it decided.
    
    For example instead of just saying "this customer has 75% churn risk", 
    it tells you "the main reason is their month-to-month contract and high monthly charges."
    
    This helps your team take the right action, not just a generic one.
    """)

with st.expander("What happens when I click Approve & Send?"):
    st.markdown("""
    The retention email drafted by the AI is sent directly to the customer's email address 
    you provide. You can edit the subject and body before sending.
    
    Nothing is sent automatically — a human always reviews and approves first. 
    This is called **Human-in-the-Loop** and is a key safety pattern in production AI systems.
    """)

with st.expander("Can I use my own customer data?"):
    st.markdown("""
    Yes! Use the **Batch CSV Upload** tab to upload your own customer database.
    The agent will analyze every row and return a full risk table.
    
    The CSV needs columns like: tenure, contract type, monthly charges, and services used.
    Text values like "Yes/No" are handled automatically.
    """)
# ── Footer ────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.85em;'>
Built with &nbsp;
🦜 LangGraph &nbsp;·&nbsp; 
⚡ Groq &nbsp;·&nbsp; 
🌲 Scikit-learn &nbsp;·&nbsp; 
📊 SHAP &nbsp;·&nbsp; 
🚀 FastAPI &nbsp;·&nbsp; 
🎨 Streamlit
</div>
""", unsafe_allow_html=True)