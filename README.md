# 🛡️ RiskGuard AI — Explainable Fraud & Regulatory Intelligence Copilot

> **From risk signal → evidence → regulatory guidance → investigation finding**

RiskGuard AI is an explainable financial-risk investigation copilot built with **Snowflake, Snowflake Cortex, and Streamlit**.

It helps banking and financial-services analysts investigate potential risk by combining deterministic transaction-risk signals, customer/account data, transaction evidence, and synthetic regulatory guidance in one workflow.

**Important:** RiskGuard AI does not determine that fraud has occurred. It identifies risk signals and supports human-led investigation.

---

## 🎯 Problem

Financial institutions need to monitor large volumes of transactions for potential fraud, AML, and other regulatory risks.

Traditional investigation workflows can require analysts to:

* Identify suspicious transaction patterns
* Collect supporting transaction evidence
* Search regulatory guidance
* Understand why an alert was generated
* Document investigation findings
* Prepare audit-ready records

These activities can be fragmented and time-consuming.

RiskGuard AI brings these steps together into a single investigation workflow.

---

## 💡 Solution

RiskGuard AI combines:

**Deterministic risk detection + Snowflake analytics + regulatory search + Cortex AI + human analyst review**

The workflow is:

```text
Transaction / Customer Data
          ↓
Deterministic Risk Rules
          ↓
Risk Signals
          ↓
Evidence & Transaction Timeline
          ↓
Regulatory Guidance
          ↓
Cortex AI Investigation
          ↓
Audit-Ready Finding
          ↓
Human Analyst Decision
```

The AI explains and connects evidence; it does **not** independently decide whether fraud occurred.

---

## 🚀 Key Features

### 📊 Risk Command Center

Provides an executive overview of:

* Total customers
* High-risk customers
* Flagged customers
* Total transaction value
* High-value transaction value

### 🚨 Deterministic Risk Detection

Risk signals are generated using transparent SQL-based rules.

Examples include:

* High-value transaction velocity
* High-value international transactions
* Activity involving customers classified as high risk

Each signal receives a severity and risk score.

### 🔎 Customer Investigation

Analysts can select a customer and view:

* Customer profile
* KYC status
* Risk level
* Risk score
* Detected risk signals
* Transaction evidence
* Transaction timeline

### 📚 Regulatory Intelligence

Synthetic regulatory guidance is indexed using **Snowflake Cortex Search**.

Risk evidence is mapped to relevant guidance such as:

* High-value transaction monitoring
* International transaction monitoring
* Customer risk and enhanced due diligence
* Suspicious activity review
* Investigation documentation and audit evidence

### 🤖 AI Investigation Copilot

**Snowflake Cortex Agent** orchestrates:

* Cortex Analyst for structured risk analytics
* Cortex Search for regulatory guidance
* Evidence-backed investigation reasoning

The AI produces:

* Investigation finding
* Risk signals
* Transaction evidence
* Regulatory guidance
* Recommended actions
* Investigation decision position

### 📄 Audit-Ready Investigation Report

The application provides an investigation summary that can be downloaded for documentation and review.

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │   Risk Command      │
                    │      Center         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Cortex Agent      │
                    │  Investigation      │
                    │    Orchestration    │
                    └───────┬─────┬───────┘
                            │     │
                 ┌──────────┘     └──────────┐
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │ Cortex Analyst  │         │  Cortex Search  │
        │ Structured Risk │         │ Regulatory      │
        │ Analytics       │         │ Intelligence    │
        └────────┬────────┘         └────────┬────────┘
                 │                           │
                 ▼                           ▼
        ┌────────────────────────────────────────────┐
        │              Snowflake Data Layer          │
        │                                            │
        │ CUSTOMERS                                  │
        │ ACCOUNTS                                   │
        │ TRANSACTIONS                               │
        │ RISK_SIGNALS                               │
        │ INVESTIGATIONS                             │
        │ REGULATORY_DOCUMENTS                       │
        └────────────────────────────────────────────┘
```

---

# ❄️ Snowflake Technologies

RiskGuard AI uses the following Snowflake capabilities:

| Snowflake Technology | Purpose                                   |
| -------------------- | ----------------------------------------- |
| Snowflake Tables     | Customer, account and transaction data    |
| SQL                  | Deterministic risk detection              |
| Views                | Dashboard and investigation analytics     |
| Semantic View        | Structured data model for Cortex Analyst  |
| Cortex Analyst       | Natural-language structured data analysis |
| Cortex Search        | Regulatory document retrieval             |
| Cortex Agent         | AI investigation orchestration            |
| Streamlit            | Interactive investigation interface       |
| Snowflake Warehouse  | Query execution                           |

---

# 🗄️ Data Model

The prototype uses synthetic banking data.

### CUSTOMERS

Contains:

* Customer ID
* Customer name
* Location
* Occupation
* Customer risk level
* KYC status

### ACCOUNTS

Contains:

* Account ID
* Customer ID
* Account type
* Balance
* Account status

### TRANSACTIONS

Contains:

* Transaction ID
* Customer/account
* Timestamp
* Amount
* Merchant
* Beneficiary
* Beneficiary country
* Channel
* Transaction status

### RISK_SIGNALS

Stores:

* Signal type
* Severity
* Risk score
* Description
* Detection timestamp

### INVESTIGATIONS

Stores investigation status, findings and recommended actions.

### REGULATORY_DOCUMENTS

Contains synthetic regulatory and compliance guidance used by Cortex Search.

---

# 🧠 Risk Detection Logic

Risk detection is deliberately separated from generative AI.

Example:

```text
3+ high-value transactions
        ↓
Potential velocity signal
        ↓
Risk score
        ↓
Investigation
```

Another example:

```text
High-value transaction
+
International beneficiary
        ↓
Potential international-risk signal
        ↓
Regulatory guidance retrieval
        ↓
Analyst review
```

This design prevents the LLM from being responsible for the initial fraud/risk determination.

---

# 🤖 AI Architecture

RiskGuard AI uses three Cortex capabilities.

### Cortex Analyst

Converts natural-language investigation questions into structured analytical queries against the RiskGuard semantic view.

Example:

> "Why was customer CUST1004 flagged?"

The system retrieves customer-level risk and transaction metrics.

### Cortex Search

Searches the synthetic regulatory guidance corpus for relevant evidence.

Example:

> "What guidance applies to high-value international transactions?"

### Cortex Agent

Combines structured analytics and regulatory intelligence to generate an evidence-backed investigation response.

---

# 🛡️ Responsible AI & Governance

RiskGuard AI follows a human-in-the-loop approach.

### The system does NOT:

* Declare a customer guilty of fraud
* Treat a risk signal as confirmed financial crime
* Infer risk from occupation or demographics
* Invent regulatory requirements
* Invent transaction evidence

### The system DOES:

* Surface deterministic risk signals
* Show supporting evidence
* Retrieve relevant guidance
* Explain why an investigation is recommended
* Identify uncertainty
* Keep the final decision with the human analyst

The application uses terminology such as:

> **Potential suspicious activity**

> **Risk signal**

> **Review required**

> **Requires investigation**

rather than making unsupported fraud determinations.

---

# 🔍 Example Investigation

Example customer:

**CUST1004 — Arjun Reddy**

The system identifies:

* HIGH customer risk level
* Risk score: **90**
* 3 detected risk signals
* 4 high-value transactions
* High-value transaction amount: **₹10.32M**
* KYC status: VERIFIED

RiskGuard AI then connects the evidence with relevant synthetic guidance and recommends enhanced analyst review.

The result is an investigation workflow rather than an automated fraud verdict.

---

# 📱 Application Workflow

The prototype provides:

```text
Risk Command Center
        ↓
High-Risk Customer Selection
        ↓
Investigation Case
        ↓
Executive Risk Summary
        ↓
Risk Evidence
        ↓
Detected Risk Signals
        ↓
Transaction Timeline
        ↓
Evidence → Regulatory Guidance
        ↓
AI Investigation Report
        ↓
Downloadable Finding
```

---

# 🏆 Why RiskGuard AI?

The key differentiator is the connection between **risk detection and explainability**.

Many systems can identify an unusual transaction.

RiskGuard AI goes further:

```text
SIGNAL
  ↓
EVIDENCE
  ↓
REGULATORY GUIDANCE
  ↓
EXPLANATION
  ↓
INVESTIGATION FINDING
  ↓
HUMAN DECISION
```

This makes the workflow more useful for real-world financial-risk investigations.

---

# 🧪 Prototype Data

All customer, account and transaction records are **synthetic**.

The regulatory guidance used by the prototype is also **synthetic guidance created for demonstration purposes**.

No real customer information is used.

---

# 🔮 Future Enhancements

Potential production enhancements include:

* Real-time transaction streaming
* Advanced anomaly detection
* ML-based risk scoring
* Graph-based relationship analysis
* Case-management integration
* Role-based access control
* Production regulatory sources
* Automated alert prioritization
* Model monitoring and explainability
* Integration with banking transaction systems

---

# ⚠️ Disclaimer

RiskGuard AI is a hackathon prototype using synthetic data and synthetic regulatory guidance.

It is designed to demonstrate an explainable risk-investigation workflow and is **not a production fraud-detection or regulatory-compliance system**.

Risk signals are investigation triggers and do not establish confirmed fraud or financial crime.

---

# 🏁 Hackathon Value Proposition

**RiskGuard AI turns financial risk signals into evidence-backed investigations by combining Snowflake analytics, Cortex AI, regulatory search, and human-in-the-loop decision support.**

The architecture demonstrates how Snowflake can provide a governed foundation for combining structured financial data, regulatory intelligence and AI-assisted investigation in a single workflow.

