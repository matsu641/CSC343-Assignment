-- Customer Appreciation Week

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;


-- Insert the free mug item with next available IID
INSERT INTO Item (IID, category, description, price)
SELECT COALESCE(MAX(IID), 0) + 1, 'Housewares', 'Company logo mug', 0
FROM Item;

-- For each customer who ordered yesterday, find their first
-- purchase (lowest checkout_time, ties broken by lowest PID)
DROP VIEW IF EXISTS FirstYesterdayPurchase CASCADE;
CREATE VIEW FirstYesterdayPurchase AS
SELECT DISTINCT ON (CID) CID, PID
FROM Purchase
WHERE checkout_time::date = (CURRENT_DATE - INTERVAL '1 day')::date
ORDER BY CID, checkout_time, PID;

-- Add the free mug as a line item to those purchases
-- Look up the mug's IID by its description to avoid view re-evaluation
INSERT INTO LineItem (PID, IID, quantity)
SELECT fyp.PID, i.IID, 1
FROM FirstYesterdayPurchase fyp
CROSS JOIN (SELECT IID FROM Item WHERE description = 'Company logo mug') i;
