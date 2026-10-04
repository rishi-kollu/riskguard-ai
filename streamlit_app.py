import json
import streamlit as st
from snowflake.snowpark.context import get_active_session

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="RiskGuard AI",
    page_icon="🛡️",
    layout="wide"
)

session = get_active_session()

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🛡️ RiskGuard AI")
st.subheader("Explainable Fraud & Regulatory Intelligence Copilot")

st.caption(
    "Detect risk signals • Explain evidence • Retrieve regulatory guidance • "
    "Support investigation decisions"
)

st.divider()

# ---------------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------------

metrics = session.sql("""
    SELECT
        TOTAL_CUSTOMERS,
        HIGH_RISK_CUSTOMERS,
        FLAGGED_CUSTOMERS,
        TOTAL_TRANSACTION_VALUE,
        HIGH_VALUE_TRANSACTION_VALUE
    FROM RISKGUARD_DB.RISK.DASHBOARD_METRICS
""").collect()[0]

total_customers = metrics["TOTAL_CUSTOMERS"]
high_risk_customers = metrics["HIGH_RISK_CUSTOMERS"]
flagged_customers = metrics["FLAGGED_CUSTOMERS"]
total_transaction_value = metrics["TOTAL_TRANSACTION_VALUE"]
high_value_transaction_value = metrics["HIGH_VALUE_TRANSACTION_VALUE"]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("👥 Customers", f"{total_customers:,}")

with col2:
    st.metric("🔴 High Risk", f"{high_risk_customers:,}")

with col3:
    st.metric("🚨 Flagged", f"{flagged_customers:,}")

with col4:
    st.metric(
        "💰 Transaction Value",
        f"₹{float(total_transaction_value):,.0f}"
    )

with col5:
    st.metric(
        "⚠️ High-Value",
        f"₹{float(high_value_transaction_value):,.0f}"
    )

st.divider()

# ---------------------------------------------------------
# HIGH-RISK CUSTOMERS
# ---------------------------------------------------------

st.header("🚨 High-Risk Customers")

high_risk_df = session.sql("""
    SELECT
        CUSTOMER_ID,
        CUSTOMER_NAME,
        CITY,
        OCCUPATION,
        CUSTOMER_RISK_LEVEL,
        KYC_STATUS,
        TOTAL_TRANSACTIONS,
        TOTAL_TRANSACTION_AMOUNT,
        HIGH_VALUE_TRANSACTION_COUNT,
        HIGH_VALUE_TRANSACTION_AMOUNT,
        RISK_SIGNAL_COUNT,
        MAX_RISK_SCORE
    FROM RISKGUARD_DB.RISK.HIGH_RISK_CUSTOMERS
    ORDER BY MAX_RISK_SCORE DESC, RISK_SIGNAL_COUNT DESC
""").to_pandas()

st.dataframe(
    high_risk_df,
    width="stretch",
    hide_index=True
)

st.divider()

# ---------------------------------------------------------
# CUSTOMER INVESTIGATION
# ---------------------------------------------------------

st.header("🔎 Customer Investigation")

customer_options = high_risk_df["CUSTOMER_ID"].tolist()

selected_customer = st.selectbox(
    "Select a customer to investigate",
    customer_options
)

selected_row = high_risk_df[
    high_risk_df["CUSTOMER_ID"] == selected_customer
].iloc[0]

# Customer overview

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Customer",
        selected_row["CUSTOMER_NAME"]
    )

with col2:
    st.metric(
        "Risk Score",
        int(selected_row["MAX_RISK_SCORE"])
    )

with col3:
    st.metric(
        "Risk Signals",
        int(selected_row["RISK_SIGNAL_COUNT"])
    )

with col4:
    st.metric(
        "KYC Status",
        selected_row["KYC_STATUS"]
    )

st.write(
    f"**Location:** {selected_row['CITY']}  |  "
    f"**Occupation:** {selected_row['OCCUPATION']}"
)
# ---------------------------------------------------------
# INVESTIGATION CASE SUMMARY
# ---------------------------------------------------------

st.subheader("📁 Investigation Case")

case_col1, case_col2, case_col3 = st.columns(3)

with case_col1:
    st.metric(
        "Case Status",
        "REVIEW REQUIRED"
    )

with case_col2:
    st.metric(
        "Risk Level",
        selected_row["CUSTOMER_RISK_LEVEL"]
    )

with case_col3:
    st.metric(
        "Evidence Strength",
        "HIGH"
    )

st.warning(
    f"Customer {selected_customer} requires analyst review because "
    f"{int(selected_row['RISK_SIGNAL_COUNT'])} risk signal(s) were detected "
    f"across {int(selected_row['TOTAL_TRANSACTIONS'])} transaction(s). "
    "This is an investigation trigger, not a confirmed fraud finding."
)
# ---------------------------------------------------------
# EXECUTIVE RISK SUMMARY
# ---------------------------------------------------------

st.subheader("📌 Executive Risk Summary")

summary_col1, summary_col2 = st.columns([2, 1])

with summary_col1:

    executive_summary = f"""
**{selected_row["CUSTOMER_NAME"]} ({selected_customer})** requires
enhanced analyst review based on **{int(selected_row["RISK_SIGNAL_COUNT"])}**
detected risk signal(s) across **{int(selected_row["TOTAL_TRANSACTIONS"])}**
transaction(s).

The customer has a risk score of **{int(selected_row["MAX_RISK_SCORE"])}**
and **{int(selected_row["HIGH_VALUE_TRANSACTION_COUNT"])} high-value
transaction(s)** totaling
**₹{float(selected_row["HIGH_VALUE_TRANSACTION_AMOUNT"]):,.0f}**.

KYC status is **{selected_row["KYC_STATUS"]}**.

The detected activity should be reviewed against the customer's expected
profile, transaction purpose, source of funds, counterparties, and
applicable regulatory guidance.
"""

    st.markdown(executive_summary)

with summary_col2:

    st.warning(
        "REVIEW REQUIRED\n\n"
        "Enhanced analyst review is recommended."
    )

    st.caption(
        "AI-assisted summary • Evidence-backed • "
        "Not a final fraud determination"
    )

# ---------------------------------------------------------
# RISK EVIDENCE
# ---------------------------------------------------------

st.subheader("📊 Risk Evidence")

evidence_col1, evidence_col2, evidence_col3 = st.columns(3)

with evidence_col1:
    st.metric(
        "Transactions",
        int(selected_row["TOTAL_TRANSACTIONS"])
    )

with evidence_col2:
    st.metric(
        "High-Value Transactions",
        int(selected_row["HIGH_VALUE_TRANSACTION_COUNT"])
    )

with evidence_col3:
    st.metric(
        "High-Value Amount",
        f"₹{float(selected_row['HIGH_VALUE_TRANSACTION_AMOUNT']):,.0f}"
    )
# ---------------------------------------------------------
# ANALYST CASE FINDING
# ---------------------------------------------------------

st.subheader("📝 Preliminary Case Finding")

finding_text = f"""
**Customer:** {selected_row["CUSTOMER_NAME"]} ({selected_customer})

**Finding:** Risk signals indicate activity requiring enhanced
investigation. The customer has a risk score of
**{int(selected_row["MAX_RISK_SCORE"])}** and
**{int(selected_row["RISK_SIGNAL_COUNT"])} detected risk signal(s)**.

**Transaction Evidence:** The customer has completed
**{int(selected_row["TOTAL_TRANSACTIONS"])} transaction(s)**, including
**{int(selected_row["HIGH_VALUE_TRANSACTION_COUNT"])} high-value
transaction(s)** totaling
**₹{float(selected_row["HIGH_VALUE_TRANSACTION_AMOUNT"]):,.0f}**.

**KYC:** {selected_row["KYC_STATUS"]}

**Investigation Position:** The available evidence supports
**enhanced analyst review**. The available data does not establish
confirmed fraud or financial crime.
"""

st.markdown(finding_text)

# ---------------------------------------------------------
# DETECTED RISK SIGNALS
# ---------------------------------------------------------

st.subheader("🚨 Detected Risk Signals")

signals_df = session.sql(f"""
    SELECT
        SIGNAL_ID,
        SIGNAL_TYPE,
        SEVERITY,
        RISK_SCORE,
        DESCRIPTION,
        DETECTED_AT
    FROM RISKGUARD_DB.RISK.RISK_SIGNALS
    WHERE CUSTOMER_ID = '{selected_customer}'
    ORDER BY RISK_SCORE DESC
""").to_pandas()

if len(signals_df) > 0:
    st.dataframe(
        signals_df,
        width="stretch",
        hide_index=True
    )
else:
    st.info("No risk signals found.")
# ---------------------------------------------------------
# TRANSACTION TIMELINE
# ---------------------------------------------------------

st.subheader("🕒 Transaction Timeline")

transactions_df = session.sql(f"""
    SELECT
        TRANSACTION_ID,
        TRANSACTION_DATE,
        TRANSACTION_TYPE,
        AMOUNT,
        MERCHANT,
        BENEFICIARY_ACCOUNT,
        BENEFICIARY_COUNTRY,
        CHANNEL,
        TRANSACTION_STATUS
    FROM RISKGUARD_DB.RISK.TRANSACTIONS
    WHERE CUSTOMER_ID = '{selected_customer}'
    ORDER BY TRANSACTION_DATE
""").to_pandas()

if len(transactions_df) > 0:

    st.dataframe(
        transactions_df,
        width="stretch",
        hide_index=True
    )

else:
    st.info("No transactions found.")
# ---------------------------------------------------------
# EVIDENCE → REGULATORY POLICY MAPPING
# ---------------------------------------------------------

st.subheader("📚 Evidence → Regulatory Guidance")

st.caption(
    "Maps detected risk signals to the relevant synthetic regulatory "
    "guidance and recommended investigation focus."
)

# Determine which guidance applies based on the customer's signals
signal_types = signals_df["SIGNAL_TYPE"].astype(str).str.upper().tolist()

policy_rows = []

# High-value transaction monitoring
if any(
    "HIGH_VALUE" in signal or "VELOCITY" in signal
    for signal in signal_types
):
    policy_rows.append({
        "Risk Signal": "High-Value / Velocity Activity",
        "Evidence": (
            f"{int(selected_row['HIGH_VALUE_TRANSACTION_COUNT'])} "
            f"high-value transactions totaling "
            f"₹{float(selected_row['HIGH_VALUE_TRANSACTION_AMOUNT']):,.0f}"
        ),
        "Relevant Guidance": "REG-AML-001",
        "Investigation Focus": (
            "Review transaction pattern, source of funds, "
            "purpose of transactions, and expected customer activity."
        )
    })

# International transaction monitoring
international_activity = session.sql(f"""
    SELECT COUNT(*) AS INTERNATIONAL_COUNT
    FROM RISKGUARD_DB.RISK.TRANSACTIONS
    WHERE CUSTOMER_ID = '{selected_customer}'
      AND UPPER(BENEFICIARY_COUNTRY) <> 'IN'
""").collect()[0]["INTERNATIONAL_COUNT"]

if international_activity > 0:
    policy_rows.append({
        "Risk Signal": "International Transaction Activity",
        "Evidence": (
            f"{int(international_activity)} transaction(s) "
            "involving a foreign beneficiary country"
        ),
        "Relevant Guidance": "REG-AML-002",
        "Investigation Focus": (
            "Review counterparties, beneficiary geography, "
            "transaction purpose, and customer profile consistency."
        )
    })

# High-risk customer / EDD
if str(selected_row["CUSTOMER_RISK_LEVEL"]).upper() == "HIGH":
    policy_rows.append({
        "Risk Signal": "High-Risk Customer",
        "Evidence": (
            f"Customer risk classification: "
            f"{selected_row['CUSTOMER_RISK_LEVEL']}"
        ),
        "Relevant Guidance": "REG-KYC-001",
        "Investigation Focus": (
            "Perform enhanced due diligence and review "
            "significant activity against the expected profile."
        )
    })

# Suspicious activity review
if int(selected_row["RISK_SIGNAL_COUNT"]) > 0:
    policy_rows.append({
        "Risk Signal": "Multiple Risk Signals",
        "Evidence": (
            f"{int(selected_row['RISK_SIGNAL_COUNT'])} detected "
            "risk signal(s)"
        ),
        "Relevant Guidance": "REG-AML-003",
        "Investigation Focus": (
            "Review transaction history, counterparties, geography, "
            "supporting documents, and analyst reasoning."
        )
    })

if policy_rows:

    policy_df = __import__("pandas").DataFrame(policy_rows)

    st.dataframe(
        policy_df,
        width="stretch",
        hide_index=True
    )

else:
    st.info(
        "No specific regulatory guidance mapping was triggered "
        "for this customer."
    )
st.divider()

# ---------------------------------------------------------
# RISKGUARD AI
# ---------------------------------------------------------

st.header("🤖 Ask RiskGuard")

question = st.text_area(
    "Ask a question about this customer or their regulatory risk",
    value=f"Why was customer {selected_customer} flagged?",
    height=100
)

# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def extract_agent_text(raw_response):
    """
    Extract readable assistant text from the Cortex Agent
    JSON response instead of displaying the raw execution JSON.
    """

    try:
        if isinstance(raw_response, str):
            payload = json.loads(raw_response)
        else:
            payload = raw_response

        content = payload.get("content", [])

        text_parts = []

        for item in content:

            if item.get("type") == "text":

                text_value = item.get("text", "")

                if not text_value:
                    continue

                # Remove orchestration timeout message
                if "I've reached the time limit" in text_value:
                    continue

                text_parts.append(text_value)

        if text_parts:
            return "\n\n".join(text_parts)

        return str(raw_response)

    except Exception:
        return str(raw_response)


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

if st.button(
    "🔍 Analyze with RiskGuard",
    type="primary"
):

    with st.spinner(
        "RiskGuard is analyzing risk data and regulatory guidance..."
    ):

        request = f"""
Analyze customer {selected_customer}.

User question:
{question}

Return an investigation-oriented answer using these sections:

## Investigation Finding

Give a concise overall finding based only on available evidence.

## Risk Signals

List the detected risk signals and their severity/risk scores.

## Transaction Evidence

Explain the relevant transaction evidence, including transaction
counts, amounts, high-value activity, international activity, and
other directly supported facts.

## Regulatory Guidance

Use the retrieved regulatory guidance to explain which monitoring,
KYC/EDD, suspicious activity review, or audit requirements are relevant.

## Recommended Actions

Give practical investigation steps an analyst should take next.

## Decision

State whether the case should be:
- REVIEW REQUIRED
- ENHANCED DUE DILIGENCE
- NO FURTHER ACTION

Choose only based on the evidence available.

Important rules:

1. Risk signals do NOT prove fraud or financial crime.
2. Never state that the customer committed fraud.
3. Use language such as "potential suspicious activity",
   "risk signal", "requires investigation", or "review required".
4. Do not infer risk from occupation, nationality, city, age, or
   other demographic/profile attributes unless the data or retrieved
   regulatory guidance explicitly supports that inference.
5. If occupation is mentioned, treat it as profile context only.
6. Separate factual transaction evidence from regulatory guidance.
7. Do not invent transactions, regulations, laws, or evidence.
8. Clearly identify uncertainty when evidence is incomplete.
9. Maintain an audit-ready and professional tone.
"""

        result = session.sql(
            """
            SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
                'RISKGUARD_DB.RISK.RISKGUARD_AGENT',
                ?,
                TRUE
            ) AS RESPONSE
            """,
            params=[
                json.dumps({
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": request
                                }
                            ]
                        }
                    ]
                })
            ]
        ).collect()[0]["RESPONSE"]

    # -----------------------------------------------------
    # EXTRACT READABLE AI RESPONSE
    # -----------------------------------------------------

    analysis_text = extract_agent_text(result)

    # -----------------------------------------------------
    # INVESTIGATION STATUS
    # -----------------------------------------------------

    st.subheader("📋 Investigation Status")

    st.warning(
        "⚠️ REVIEW REQUIRED — RiskGuard detected risk signals "
        "that require analyst investigation. This is not a confirmed "
        "fraud determination."
    )

    # -----------------------------------------------------
    # AI ANALYSIS
    # -----------------------------------------------------

    st.subheader("🧠 RiskGuard Investigation Report")

    st.markdown(analysis_text)

    # -----------------------------------------------------
    # AUDIT DISCLAIMER
    # -----------------------------------------------------

    st.divider()

    st.subheader("🛡️ Investigation Disclaimer")

    st.info(
        "RiskGuard AI provides explainable investigation support using "
        "synthetic transaction data and synthetic regulatory guidance. "
        "Risk signals are indicators requiring review and do not by "
        "themselves establish fraud, money laundering, or other "
        "financial crime."
    )

    # -----------------------------------------------------
    # DOWNLOAD AUDIT REPORT
    # -----------------------------------------------------

    report_text = f"""
RISKGUARD AI — INVESTIGATION REPORT
====================================

Customer: {selected_customer}
Customer Name: {selected_row["CUSTOMER_NAME"]}

Risk Score: {int(selected_row["MAX_RISK_SCORE"])}
Risk Signals: {int(selected_row["RISK_SIGNAL_COUNT"])}
KYC Status: {selected_row["KYC_STATUS"]}

Transactions: {int(selected_row["TOTAL_TRANSACTIONS"])}
High-Value Transactions: {int(selected_row["HIGH_VALUE_TRANSACTION_COUNT"])}
High-Value Amount: ₹{float(selected_row["HIGH_VALUE_TRANSACTION_AMOUNT"]):,.0f}

------------------------------------
AI INVESTIGATION ANALYSIS
------------------------------------

{analysis_text}

------------------------------------
DISCLAIMER
------------------------------------

Risk signals are indicators requiring investigation and do not
constitute a confirmed determination of fraud or financial crime.

Generated by RiskGuard AI.
Synthetic data and synthetic regulatory guidance used for demonstration.
"""

    st.download_button(
        label="📥 Download Investigation Report",
        data=report_text,
        file_name=f"RiskGuard_{selected_customer}_Investigation.txt",
        mime="text/plain"
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "RiskGuard AI • Snowflake Cortex • Synthetic financial data • "
    "AI-assisted investigation support, not a final fraud determination"
)