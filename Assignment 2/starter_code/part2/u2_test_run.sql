SET SEARCH_PATH TO Recommender;

BEGIN;

-- Create test customer and item
INSERT INTO Customer (CID,email,last_name,first_name) VALUES (9999,'t@test','T','Test') ON CONFLICT DO NOTHING;
INSERT INTO Item (IID,category,description,price) VALUES (9999,'test','test item',10.0) ON CONFLICT DO NOTHING;

-- Create 7 purchases with same card_pan spaced by time
INSERT INTO Purchase (PID,CID,checkout_time,card_pan,card_type) VALUES
 (9000001,9999, NOW() - INTERVAL '6 hours', 'PAN_TEST','visa'),
 (9000002,9999, NOW() - INTERVAL '5 hours', 'PAN_TEST','visa'),
 (9000003,9999, NOW() - INTERVAL '4 hours', 'PAN_TEST','visa'),
 (9000004,9999, NOW() - INTERVAL '3 hours', 'PAN_TEST','visa'),
 (9000005,9999, NOW() - INTERVAL '2 hours', 'PAN_TEST','visa'),
 (9000006,9999, NOW() - INTERVAL '1 hour',  'PAN_TEST','visa'),
 (9000007,9999, NOW() - INTERVAL '30 minutes','PAN_TEST','visa')
ON CONFLICT DO NOTHING;

-- add one LineItem per purchase
INSERT INTO LineItem (PID,IID,quantity) VALUES
 (9000001,9999,1),(9000002,9999,1),(9000003,9999,1),(9000004,9999,1),(9000005,9999,1),(9000006,9999,1),(9000007,9999,1)
ON CONFLICT DO NOTHING;

-- Show before
\echo '--- BEFORE ---'
SELECT PID, checkout_time FROM Purchase WHERE card_pan='PAN_TEST' ORDER BY checkout_time;

-- Run u2 logic: find PIDs to delete (rn > 5 per card_pan in last 24 hours)
DROP VIEW IF EXISTS IntermediateStep CASCADE;
CREATE VIEW IntermediateStep AS
SELECT PID
FROM (
    SELECT PID,
           ROW_NUMBER() OVER (PARTITION BY card_pan ORDER BY checkout_time) AS rn
    FROM Purchase
    WHERE checkout_time >= NOW() - INTERVAL '24 hours'
) t
WHERE rn > 5;

DELETE FROM LineItem
WHERE PID IN (SELECT PID FROM IntermediateStep);

DELETE FROM Purchase
WHERE PID IN (SELECT PID FROM IntermediateStep);

-- Show after
\echo '--- AFTER ---'
SELECT PID, checkout_time FROM Purchase WHERE card_pan='PAN_TEST' ORDER BY checkout_time;
SELECT * FROM LineItem WHERE PID BETWEEN 9000001 AND 9000007 ORDER BY PID;

COMMIT;
