-- Fraud Prevention

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps. (But give them better names!)
DROP VIEW IF EXISTS IntermediateStep CASCADE;

-- Define views for your intermediate steps here:
CREATE VIEW IntermediateStep AS
SELECT PID
FROM (
	SELECT PID,
		   ROW_NUMBER() OVER (PARTITION BY card_pan ORDER BY checkout_time) AS rn
	FROM Purchase
	WHERE checkout_time >= NOW() - INTERVAL '24 hours'
) t
WHERE rn > 5;

-- Delete line items for purchases that exceed the 5-per-card limit in the
-- last 24 hours, then delete the purchases themselves.
DELETE FROM LineItem
WHERE PID IN (SELECT PID FROM IntermediateStep);

DELETE FROM Purchase
WHERE PID IN (SELECT PID FROM IntermediateStep);
