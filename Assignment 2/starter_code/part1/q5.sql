-- Hyperconsumers

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q5 CASCADE;

CREATE TABLE q5 (
    year VARCHAR(4) NOT NULL,
    name VARCHAR(65) NOT NULL,
    email VARCHAR(300) NOT NULL,
    items INTEGER NOT NULL
);

-- Total units bought per customer per year
DROP VIEW IF EXISTS YearlyUnits CASCADE;
CREATE VIEW YearlyUnits AS
SELECT to_char(EXTRACT(YEAR FROM p.checkout_time), 'FM0000')
    AS year,
    p.CID,
    SUM(li.quantity) AS total_units
FROM Purchase p
JOIN LineItem li ON p.PID = li.PID
GROUP BY EXTRACT(YEAR FROM p.checkout_time), p.CID;

-- Rank the total units within each year using DENSE_RANK
DROP VIEW IF EXISTS RankedConsumers CASCADE;
CREATE VIEW RankedConsumers AS
SELECT year, CID, total_units,
    DENSE_RANK() OVER (
        PARTITION BY year ORDER BY total_units DESC
    ) AS rank
FROM YearlyUnits;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q5
SELECT r.year,
    c.first_name || ' ' || c.last_name AS name,
    c.email,
    r.total_units AS items
FROM RankedConsumers r
JOIN Customer c ON r.CID = c.CID
WHERE r.rank <= 5;
