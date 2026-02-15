-- Unrated products


-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF exists q1 CASCADE;

CREATE TABLE q1(
    CID INTEGER,
    first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
    email TEXT	
);

-- Items that have zero reviews (no row in Review at all)
DROP VIEW IF EXISTS UnratedItems CASCADE;
CREATE VIEW UnratedItems AS
SELECT IID
FROM Item
WHERE IID NOT IN (SELECT IID FROM Review);

-- Each (customer, unrated item) pair where the customer bought that item
DROP VIEW IF EXISTS CustomerUnratedPurchases CASCADE;
CREATE VIEW CustomerUnratedPurchases AS
SELECT DISTINCT p.CID, li.IID
FROM Purchase p
JOIN LineItem li ON p.PID = li.PID
WHERE li.IID IN (SELECT IID FROM UnratedItems);

-- Customers who bought at least 3 different unrated items
DROP VIEW IF EXISTS QualifiedCustomers CASCADE;
CREATE VIEW QualifiedCustomers AS
SELECT CID
FROM CustomerUnratedPurchases
GROUP BY CID
HAVING COUNT(DISTINCT IID) >= 3;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q1
SELECT c.CID, c.first_name, c.last_name, c.email
FROM Customer c
WHERE c.CID IN (SELECT CID FROM QualifiedCustomers);