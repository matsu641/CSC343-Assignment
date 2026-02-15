--Year-over-year sales

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q6 CASCADE;

CREATE TABLE q6 (
    IID INT NOT NULL,
    year1 INT NOT NULL,
    year1_avg FLOAT NOT NULL,
    year2 INT NOT NULL,
    year2_avg FLOAT NOT NULL,
    yoy_change FLOAT NOT NULL
);

-- Operational year range (earliest to latest purchase year)
DROP VIEW IF EXISTS YearRange CASCADE;
CREATE VIEW YearRange AS
SELECT EXTRACT(YEAR FROM MIN(checkout_time))::INT AS min_year,
    EXTRACT(YEAR FROM MAX(checkout_time))::INT AS max_year
FROM Purchase;

-- All operational years
DROP VIEW IF EXISTS OpYears CASCADE;
CREATE VIEW OpYears AS
SELECT generate_series(min_year, max_year) AS year
FROM YearRange;

-- All 12 months
DROP VIEW IF EXISTS Months CASCADE;
CREATE VIEW Months AS
SELECT generate_series(1, 12) AS month;

-- All (item, year, month) combinations
DROP VIEW IF EXISTS AllCombos CASCADE;
CREATE VIEW AllCombos AS
SELECT i.IID, y.year, m.month
FROM Item i CROSS JOIN OpYears y CROSS JOIN Months m;

-- Actual monthly sales per item
DROP VIEW IF EXISTS MonthlySales CASCADE;
CREATE VIEW MonthlySales AS
SELECT li.IID,
    EXTRACT(YEAR FROM p.checkout_time)::INT AS year,
    EXTRACT(MONTH FROM p.checkout_time)::INT AS month,
    SUM(li.quantity) AS total_qty
FROM Purchase p
JOIN LineItem li ON p.PID = li.PID
GROUP BY li.IID,
    EXTRACT(YEAR FROM p.checkout_time),
    EXTRACT(MONTH FROM p.checkout_time);

-- Fill in zeros for missing months
DROP VIEW IF EXISTS AllMonthlySales CASCADE;
CREATE VIEW AllMonthlySales AS
SELECT ac.IID, ac.year, ac.month,
    COALESCE(ms.total_qty, 0) AS total_qty
FROM AllCombos ac
LEFT JOIN MonthlySales ms
    ON ac.IID = ms.IID
    AND ac.year = ms.year
    AND ac.month = ms.month;

-- Average unit sales per item per year (avg of 12 months)
DROP VIEW IF EXISTS YearlyAvg CASCADE;
CREATE VIEW YearlyAvg AS
SELECT IID, year,
    AVG(total_qty::FLOAT) AS avg_sales
FROM AllMonthlySales
GROUP BY IID, year;

-- Consecutive year pairs
DROP VIEW IF EXISTS YearPairs CASCADE;
CREATE VIEW YearPairs AS
SELECT y1.year AS year1, y1.year + 1 AS year2
FROM OpYears y1
JOIN OpYears y2 ON y1.year + 1 = y2.year;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q6
SELECT a1.IID,
    yp.year1,
    a1.avg_sales AS year1_avg,
    yp.year2,
    a2.avg_sales AS year2_avg,
    CASE
        WHEN a1.avg_sales = 0 AND a2.avg_sales = 0
            THEN 0
        WHEN a1.avg_sales = 0 AND a2.avg_sales > 0
            THEN 'Infinity'::FLOAT
        ELSE (a2.avg_sales - a1.avg_sales)
            / a1.avg_sales * 100
    END AS yoy_change
FROM YearPairs yp
JOIN YearlyAvg a1
    ON yp.year1 = a1.year
JOIN YearlyAvg a2
    ON yp.year2 = a2.year AND a1.IID = a2.IID;