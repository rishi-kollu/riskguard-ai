```sql id="q4zq7r"
USE DATABASE RISKGUARD_DB;
USE SCHEMA RISK;

-- ============================================
-- SEMANTIC VIEW FOR CORTEX ANALYST
-- ============================================

CREATE OR REPLACE SEMANTIC VIEW RISK_ANALYTICS

TABLES (
    risk_summary AS RISK_SUMMARY
        PRIMARY KEY (CUSTOMER_ID)
        COMMENT = 'Customer risk and transaction summary'
)

DIMENSIONS (
    risk_summary.customer_id AS CUSTOMER_ID
        COMMENT = 'Unique customer identifier',

    risk_summary.customer_name AS CUSTOMER_NAME
        COMMENT = 'Customer name',

    risk_summary.city AS CITY
        COMMENT = 'Customer city',

    risk_summary.occupation AS OCCUPATION
        COMMENT = 'Customer occupation',

    risk_summary.customer_risk_level AS CUSTOMER_RISK_LEVEL
        COMMENT = 'Customer risk classification',

    risk_summary.kyc_status AS KYC_STATUS
        COMMENT = 'Customer KYC verification status'
)

METRICS (
    risk_summary.total_transactions AS
        SUM(TOTAL_TRANSACTIONS)
        COMMENT = 'Total number of transactions',

    risk_summary.total_transaction_amount AS
        SUM(TOTAL_TRANSACTION_AMOUNT)
        COMMENT = 'Total transaction amount',

    risk_summary.high_value_transaction_count AS
        SUM(HIGH_VALUE_TRANSACTION_COUNT)
        COMMENT = 'Number of high-value transactions',

    risk_summary.high_value_transaction_amount AS
        SUM(HIGH_VALUE_TRANSACTION_AMOUNT)
        COMMENT = 'Total high-value transaction amount',

    risk_summary.risk_signal_count AS
        SUM(RISK_SIGNAL_COUNT)
        COMMENT = 'Number of risk signals',

    risk_summary.max_risk_score AS
        MAX(MAX_RISK_SCORE)
        COMMENT = 'Maximum risk score'
)

COMMENT = 'Risk analytics semantic view for RiskGuard AI';
```
