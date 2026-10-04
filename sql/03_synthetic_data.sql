```sql
USE DATABASE RISKGUARD_DB;
USE SCHEMA RISK;

-- ============================================
-- SYNTHETIC CUSTOMERS
-- ============================================

INSERT INTO CUSTOMERS VALUES
('CUST1001','Ananya Rao',34,'Hyderabad','India','Software Engineer','LOW','VERIFIED','2023-04-10'),
('CUST1002','Rahul Mehta',45,'Mumbai','India','Business Owner','MEDIUM','VERIFIED','2022-08-19'),
('CUST1003','Priya Sharma',29,'Bengaluru','India','Consultant','LOW','VERIFIED','2024-01-15'),
('CUST1004','Arjun Reddy',51,'Delhi','India','Import Export','HIGH','VERIFIED','2021-11-03'),
('CUST1005','Sneha Patel',38,'Ahmedabad','India','Jewellery Business','MEDIUM','VERIFIED','2022-06-20'),
('CUST1006','Vikram Singh',42,'Pune','India','Trader','MEDIUM','VERIFIED','2023-02-14'),
('CUST1007','Neha Kapoor',47,'Mumbai','India','Real Estate','HIGH','VERIFIED','2021-05-11'),
('CUST1008','Kiran Kumar',31,'Chennai','India','Engineer','LOW','VERIFIED','2024-02-22'),
('CUST1009','Meera Nair',36,'Kochi','India','Consultant','LOW','VERIFIED','2023-09-18'),
('CUST1010','Rohan Verma',55,'Delhi','India','Import Export','HIGH','VERIFIED','2020-12-01');


-- ============================================
-- SYNTHETIC ACCOUNTS
-- ============================================

INSERT INTO ACCOUNTS VALUES
('ACC1001','CUST1001','SAVINGS',185000,'ACTIVE'),
('ACC1002','CUST1002','CURRENT',850000,'ACTIVE'),
('ACC1003','CUST1003','SAVINGS',240000,'ACTIVE'),
('ACC1004','CUST1004','CURRENT',4200000,'ACTIVE'),
('ACC1005','CUST1005','CURRENT',1700000,'ACTIVE'),
('ACC1006','CUST1006','CURRENT',920000,'ACTIVE'),
('ACC1007','CUST1007','CURRENT',3100000,'ACTIVE'),
('ACC1008','CUST1008','SAVINGS',315000,'ACTIVE'),
('ACC1009','CUST1009','SAVINGS',275000,'ACTIVE'),
('ACC1010','CUST1010','CURRENT',5100000,'ACTIVE');


-- ============================================
-- SYNTHETIC TRANSACTIONS
-- ============================================

INSERT INTO TRANSACTIONS VALUES

('TXN001','ACC1001','CUST1001',
 '2026-09-01 09:15:00','TRANSFER',45000,
 'Domestic Transfer','BEN001','IN','ONLINE','SUCCESS'),

('TXN002','ACC1002','CUST1002',
 '2026-09-01 10:20:00','TRANSFER',125000,
 'Domestic Transfer','BEN002','IN','ONLINE','SUCCESS'),

('TXN003','ACC1003','CUST1003',
 '2026-09-01 11:05:00','TRANSFER',18000,
 'Domestic Transfer','BEN003','IN','ONLINE','SUCCESS'),

-- CUST1004: high-value velocity + international activity

('TXN004','ACC1004','CUST1004',
 '2026-09-02 08:10:00','TRANSFER',820000,
 'International Transfer','BEN004','AE','ONLINE','SUCCESS'),

('TXN005','ACC1004','CUST1004',
 '2026-09-02 10:30:00','TRANSFER',790000,
 'International Transfer','BEN005','AE','ONLINE','SUCCESS'),

('TXN006','ACC1004','CUST1004',
 '2026-09-02 13:45:00','TRANSFER',950000,
 'International Transfer','BEN006','SG','ONLINE','SUCCESS'),

('TXN007','ACC1004','CUST1004',
 '2026-09-02 17:20:00','TRANSFER',880000,
 'International Transfer','BEN007','AE','ONLINE','SUCCESS'),

-- CUST1005

('TXN008','ACC1005','CUST1005',
 '2026-09-03 09:40:00','TRANSFER',65000,
 'Domestic Transfer','BEN008','IN','ONLINE','SUCCESS'),

-- CUST1006

('TXN009','ACC1006','CUST1006',
 '2026-09-03 12:15:00','TRANSFER',95000,
 'Domestic Transfer','BEN009','IN','ONLINE','SUCCESS'),

-- CUST1007: high-value velocity

('TXN010','ACC1007','CUST1007',
 '2026-09-04 09:30:00','TRANSFER',650000,
 'Domestic Transfer','BEN010','IN','ONLINE','SUCCESS'),

('TXN011','ACC1007','CUST1007',
 '2026-09-04 10:10:00','TRANSFER',720000,
 'Domestic Transfer','BEN011','IN','ONLINE','SUCCESS'),

('TXN012','ACC1007','CUST1007',
 '2026-09-04 11:00:00','TRANSFER',680000,
 'Domestic Transfer','BEN012','IN','ONLINE','SUCCESS'),

-- CUST1008

('TXN013','ACC1008','CUST1008',
 '2026-09-05 14:20:00','TRANSFER',12000,
 'Domestic Transfer','BEN013','IN','ONLINE','SUCCESS'),

-- CUST1009

('TXN014','ACC1009','CUST1009',
 '2026-09-05 15:10:00','TRANSFER',22000,
 'Domestic Transfer','BEN014','IN','ONLINE','SUCCESS'),

-- CUST1010: high-value velocity + international activity

('TXN015','ACC1010','CUST1010',
 '2026-09-06 08:20:00','TRANSFER',1200000,
 'International Transfer','BEN015','HK','ONLINE','SUCCESS'),

('TXN016','ACC1010','CUST1010',
 '2026-09-06 11:20:00','TRANSFER',1100000,
 'International Transfer','BEN016','HK','ONLINE','SUCCESS'),

('TXN017','ACC1010','CUST1010',
 '2026-09-06 14:20:00','TRANSFER',1300000,
 'International Transfer','BEN017','HK','ONLINE','SUCCESS');
```
