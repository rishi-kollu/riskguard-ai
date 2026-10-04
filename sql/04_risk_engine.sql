```sql
USE DATABASE RISKGUARD_DB;
USE SCHEMA RISK;

-- ============================================
-- CLEAR PREVIOUS RISK SIGNALS
-- ============================================

TRUNCATE TABLE RISK_SIGNALS;


-- ============================================
-- RULE 1
-- HIGH-VALUE TRANSACTION VELOCITY
--
-- 3 or more transactions >= ₹500,000
-- within the customer transaction dataset
-- ============================================

INSERT INTO RISK_SIGNALS
(
    SIGNAL_ID,
    CUSTOMER_ID,
    ACCOUNT_ID,
    SIGNAL_TYPE,
    SEVERITY,
    RISK_SCORE,
    DESCRIPTION,
    DETECTED_AT
)
SELECT
    'SIG-VEL-' || CUSTOMER_ID,
    CUSTOMER_ID,
    MAX(ACCOUNT_ID),
    'HIGH_VALUE_VELOCITY',
    'HIGH',
    90,
    'Customer has 3 or more high-value transactions of at least ₹500,000.',
    CURRENT_TIMESTAMP()
FROM TRANSACTIONS
WHERE AMOUNT >= 500000
GROUP BY CUSTOMER_ID
HAVING COUNT(*) >= 3;


-- ============================================
-- RULE 2
-- HIGH-VALUE INTERNATIONAL TRANSACTION
--
-- Transaction >= ₹500,000 and beneficiary
-- country is outside India
-- ============================================

INSERT INTO RISK_SIGNALS
(
    SIGNAL_ID,
    CUSTOMER_ID,
    ACCOUNT_ID,
    SIGNAL_TYPE,
    SEVERITY,
    RISK_SCORE,
    DESCRIPTION,
    DETECTED_AT
)
SELECT
    'SIG-INT-' || TRANSACTION_ID,
    CUSTOMER_ID,
    ACCOUNT_ID,
    'HIGH_VALUE_INTERNATIONAL',
    'MEDIUM',
    70,
    'High-value transaction involves a beneficiary outside India.',
    CURRENT_TIMESTAMP()
FROM TRANSACTIONS
WHERE AMOUNT >= 500000
  AND BENEFICIARY_COUNTRY <> 'IN';


-- ============================================
-- RULE 3
-- HIGH-RISK CUSTOMER ACTIVITY
--
-- Customer classified HIGH and transaction
-- amount >= ₹500,000
-- ============================================

INSERT INTO RISK_SIGNALS
(
    SIGNAL_ID,
    CUSTOMER_ID,
    ACCOUNT_ID,
    SIGNAL_TYPE,
    SEVERITY,
    RISK_SCORE,
    DESCRIPTION,
    DETECTED_AT
)
SELECT
    'SIG-HRC-' || T.TRANSACTION_ID,
    T.CUSTOMER_ID,
    T.ACCOUNT_ID,
    'HIGH_RISK_CUSTOMER_ACTIVITY',
    'HIGH',
    85,
    'High-risk customer completed a transaction of at least ₹500,000.',
    CURRENT_TIMESTAMP()
FROM TRANSACTIONS T
JOIN CUSTOMERS C
    ON T.CUSTOMER_ID = C.CUSTOMER_ID
WHERE C.CUSTOMER_RISK_LEVEL = 'HIGH'
  AND T.AMOUNT >= 500000;


-- ============================================
-- CUSTOMER RISK SUMMARY
-- ============================================

CREATE OR REPLACE VIEW RISK_SUMMARY AS
SELECT
    C.CUSTOMER_ID,
    C.CUSTOMER_NAME,
    C.CITY,
    C.OCCUPATION,
    C.CUSTOMER_RISK_LEVEL,
    C.KYC_STATUS,

    COUNT(T.TRANSACTION_ID) AS TOTAL_TRANSACTIONS,

    COALESCE(
        SUM(T.AMOUNT),
        0
    ) AS TOTAL_TRANSACTION_AMOUNT,

    COUNT(
        CASE
            WHEN T.AMOUNT >= 500000
            THEN T.TRANSACTION_ID
        END
    ) AS HIGH_VALUE_TRANSACTION_COUNT,

    COALESCE(
        SUM(
            CASE
                WHEN T.AMOUNT >= 500000
                THEN T.AMOUNT
                ELSE 0
            END
        ),
        0
    ) AS HIGH_VALUE_TRANSACTION_AMOUNT,

    COUNT(DISTINCT RS.SIGNAL_ID) AS RISK_SIGNAL_COUNT,

    COALESCE(
        MAX(RS.RISK_SCORE),
        0
    ) AS MAX_RISK_SCORE

FROM CUSTOMERS C

LEFT JOIN TRANSACTIONS T
    ON C.CUSTOMER_ID = T.CUSTOMER_ID

LEFT JOIN RISK_SIGNALS RS
    ON C.CUSTOMER_ID = RS.CUSTOMER_ID

GROUP BY
    C.CUSTOMER_ID,
    C.CUSTOMER_NAME,
    C.CITY,
    C.OCCUPATION,
    C.CUSTOMER_RISK_LEVEL,
    C.KYC_STATUS;
```
