-- SALE!SALE!SALE!

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;


-- Items that have sold at least 10 units total
DROP VIEW IF EXISTS HighVolumeItems CASCADE;
CREATE VIEW HighVolumeItems AS
SELECT IID
FROM LineItem
GROUP BY IID
HAVING SUM(quantity) >= 10;

-- Apply discounts based on price range
UPDATE Item
SET price = CASE
    WHEN price >= 10 AND price <= 50 THEN price * 0.80
    WHEN price > 50 AND price <= 100 THEN price * 0.70
    WHEN price > 100 THEN price * 0.50
    ELSE price
END
WHERE IID IN (SELECT IID FROM HighVolumeItems);

