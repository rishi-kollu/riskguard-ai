```sql id="qf8k2m"
USE DATABASE RISKGUARD_DB;
USE SCHEMA RISK;

-- ============================================
-- SYNTHETIC REGULATORY GUIDANCE
-- ============================================

TRUNCATE TABLE REGULATORY_DOCUMENTS;

INSERT INTO REGULATORY_DOCUMENTS VALUES

(
    'REG-AML-001',
    'High Value Transaction Monitoring Guidance',
    'AML',
    'SYNTHETIC',
    'Financial institutions should monitor unusually large transactions and repeated high-value activity. Transactions that materially exceed expected customer activity should be reviewed for transaction purpose, source of funds, supporting documentation, and consistency with the customer profile. Potentially unusual activity should be documented for analyst review.',
    'Synthetic Guidance'
),

(
    'REG-AML-002',
    'International Transaction Monitoring Guidance',
    'AML',
    'SYNTHETIC',
    'High-value international transactions should be reviewed using a risk-based approach. Analysts should consider the transaction purpose, beneficiary information, destination jurisdiction, expected customer activity, and available supporting documentation. Cross-border activity requiring further review should be documented.',
    'Synthetic Guidance'
),

(
    'REG-KYC-001',
    'Customer Risk and Enhanced Due Diligence Guidance',
    'KYC',
    'SYNTHETIC',
    'Customers classified as higher risk may require enhanced due diligence and increased monitoring. Review teams should consider the customer risk classification, expected account activity, source of funds, transaction purpose, and relevant supporting information.',
    'Synthetic Guidance'
),

(
    'REG-AML-003',
    'Suspicious Activity Review Guidance',
    'AML',
    'SYNTHETIC',
    'Multiple risk indicators should be reviewed together rather than in isolation. Analysts should evaluate transaction patterns, customer information, counterparties, geographic factors, and available evidence before determining whether escalation is appropriate. Risk indicators alone do not establish confirmed financial crime.',
    'Synthetic Guidance'
),

(
    'REG-AUD-001',
    'Audit Evidence and Investigation Documentation',
    'AUDIT',
    'SYNTHETIC',
    'Investigation records should document the alert or risk indicator, supporting transaction evidence, relevant customer information, analytical reasoning, applicable guidance, actions taken, and final investigation disposition. Records should be sufficiently detailed to support subsequent review.',
    'Synthetic Guidance'
);


-- ============================================
-- CORTEX SEARCH SERVICE
-- ============================================

CREATE OR REPLACE CORTEX SEARCH SERVICE REGULATORY_SEARCH
    ON DOCUMENT_TEXT
    ATTRIBUTES REGULATION_AREA, JURISDICTION
    WAREHOUSE = RISKGUARD_WH
    TARGET_LAG = '1 hour'
AS
SELECT
    DOCUMENT_ID,
    DOCUMENT_TITLE,
    REGULATION_AREA,
    JURISDICTION,
    DOCUMENT_TEXT,
    SOURCE_TYPE
FROM REGULATORY_DOCUMENTS;
```
