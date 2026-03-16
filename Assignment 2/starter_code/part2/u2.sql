-- Fraud Prevention

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;


-- Cards used more than 5 times in the last 24 hours
DROP VIEW IF EXISTS OverusedCards CASCADE;
CREATE VIEW OverusedCards AS
SELECT card_pan
FROM Purchase
WHERE checkout_time > NOW() - INTERVAL '24 hours'
GROUP BY card_pan
HAVING COUNT(*) > 5;

-- For each overused card, rank purchases in last 24h by time
DROP VIEW IF EXISTS RankedPurchases CASCADE;
CREATE VIEW RankedPurchases AS
SELECT PID, card_pan,
    ROW_NUMBER() OVER (
        PARTITION BY card_pan
        ORDER BY checkout_time, PID
    ) AS rn
FROM Purchase
WHERE card_pan IN (SELECT card_pan FROM OverusedCards)
    AND checkout_time > NOW() - INTERVAL '24 hours';

-- Purchases to delete (after the 5th)
DROP VIEW IF EXISTS PurchasesToDelete CASCADE;
CREATE VIEW PurchasesToDelete AS
SELECT PID
FROM RankedPurchases
WHERE rn > 5;

-- Delete line items first (FK constraint)
DELETE FROM LineItem
WHERE PID IN (SELECT PID FROM PurchasesToDelete);

-- Then delete the purchases
DELETE FROM Purchase
WHERE PID IN (SELECT PID FROM PurchasesToDelete);
