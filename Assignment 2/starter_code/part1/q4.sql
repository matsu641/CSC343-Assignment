-- Best and Worst Categories

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q4 CASCADE;

CREATE TABLE q4 (
    month TEXT NOT NULL,
    highest_category TEXT NOT NULL,
    highest_sales_val FLOAT NOT NULL,
    lowest_category TEXT NOT NULL,
    lowest_sales_val FLOAT NOT NULL
);

-- Generate 12 months as '01' to '12'
DROP VIEW IF EXISTS Months CASCADE;
CREATE VIEW Months AS
SELECT to_char(generate_series(1, 12), 'FM09') AS month;

-- All distinct categories
DROP VIEW IF EXISTS Categories CASCADE;
CREATE VIEW Categories AS
SELECT DISTINCT category FROM Item;

-- All (month, category) combinations
DROP VIEW IF EXISTS MonthCategory CASCADE;
CREATE VIEW MonthCategory AS
SELECT month, category
FROM Months CROSS JOIN Categories;

-- Actual sales in 2024 per (month, category)
DROP VIEW IF EXISTS Sales2024 CASCADE;
CREATE VIEW Sales2024 AS
SELECT to_char(p.checkout_time, 'MM') AS month,
    i.category,
    SUM(i.price * li.quantity) AS sales_val
FROM Purchase p
JOIN LineItem li ON p.PID = li.PID
JOIN Item i ON li.IID = i.IID
WHERE EXTRACT(YEAR FROM p.checkout_time) = 2024
GROUP BY to_char(p.checkout_time, 'MM'), i.category;

-- All combinations with 0 for missing sales
DROP VIEW IF EXISTS AllSales CASCADE;
CREATE VIEW AllSales AS
SELECT mc.month, mc.category,
    COALESCE(s.sales_val, 0) AS sales_val
FROM MonthCategory mc
LEFT JOIN Sales2024 s
    ON mc.month = s.month
    AND mc.category = s.category;

-- Highest sales per month (with ties)
DROP VIEW IF EXISTS HighestPerMonth CASCADE;
CREATE VIEW HighestPerMonth AS
SELECT month, category, sales_val
FROM AllSales a
WHERE sales_val = (
    SELECT MAX(sales_val) FROM AllSales
    WHERE month = a.month
);

-- Lowest sales per month (with ties)
DROP VIEW IF EXISTS LowestPerMonth CASCADE;
CREATE VIEW LowestPerMonth AS
SELECT month, category, sales_val
FROM AllSales a
WHERE sales_val = (
    SELECT MIN(sales_val) FROM AllSales
    WHERE month = a.month
);

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q4
SELECT h.month,
    h.category AS highest_category,
    h.sales_val AS highest_sales_val,
    l.category AS lowest_category,
    l.sales_val AS lowest_sales_val
FROM HighestPerMonth h
JOIN LowestPerMonth l ON h.month = l.month;

