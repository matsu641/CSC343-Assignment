-- Curators

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q3 CASCADE;

CREATE TABLE q3 (
    CID INT NOT NULL,
    category_name TEXT NOT NULL,
    PRIMARY KEY(CID, category_name)
);

-- Number of items per category
DROP VIEW IF EXISTS CategoryItemCount CASCADE;
CREATE VIEW CategoryItemCount AS
SELECT category, COUNT(*) AS item_count
FROM Item
GROUP BY category;

-- Items a customer has bought (distinct)
DROP VIEW IF EXISTS CustomerBoughtItems CASCADE;
CREATE VIEW CustomerBoughtItems AS
SELECT DISTINCT p.CID, li.IID
FROM Purchase p
JOIN LineItem li ON p.PID = li.PID;

-- Items a customer has reviewed with a non-NULL comment
DROP VIEW IF EXISTS CustomerReviewedWithComment CASCADE;
CREATE VIEW CustomerReviewedWithComment AS
SELECT CID, IID
FROM Review
WHERE comment IS NOT NULL;

-- For each (customer, category), count how many items in that
-- category they bought AND reviewed with a comment
DROP VIEW IF EXISTS CustomerCategoryCount CASCADE;
CREATE VIEW CustomerCategoryCount AS
SELECT cb.CID, i.category,
    COUNT(DISTINCT cb.IID) AS reviewed_count
FROM CustomerBoughtItems cb
JOIN Item i ON cb.IID = i.IID
JOIN CustomerReviewedWithComment cr
    ON cb.CID = cr.CID AND cb.IID = cr.IID
GROUP BY cb.CID, i.category;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q3
SELECT cc.CID, cc.category AS category_name
FROM CustomerCategoryCount cc
JOIN CategoryItemCount ci
    ON cc.category = ci.category
WHERE cc.reviewed_count = ci.item_count;