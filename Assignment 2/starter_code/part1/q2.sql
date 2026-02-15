-- Helpfulness


-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q2 CASCADE;

create table q2(
    CID INTEGER,
    name TEXT NOT NULL,
    helpfulness_category TEXT NOT NULL
);

-- Count True/False helpfulness votes per review
DROP VIEW IF EXISTS ReviewHelpfulness CASCADE;
CREATE VIEW ReviewHelpfulness AS
SELECT reviewer AS CID, IID,
    COUNT(CASE WHEN helpfulness = True THEN 1 END)
        AS true_count,
    COUNT(CASE WHEN helpfulness = False THEN 1 END)
        AS false_count
FROM Helpfulness
GROUP BY reviewer, IID;

-- A review is "helpful" if it has been rated and
-- received more True than False
DROP VIEW IF EXISTS HelpfulReviews CASCADE;
CREATE VIEW HelpfulReviews AS
SELECT CID, IID
FROM ReviewHelpfulness
WHERE true_count > false_count;

-- Count of helpful reviews per customer
DROP VIEW IF EXISTS HelpfulCount CASCADE;
CREATE VIEW HelpfulCount AS
SELECT CID, COUNT(*) AS helpful_count
FROM HelpfulReviews
GROUP BY CID;

-- Count of total reviews written per customer
DROP VIEW IF EXISTS TotalReviewCount CASCADE;
CREATE VIEW TotalReviewCount AS
SELECT CID, COUNT(*) AS total_reviews
FROM Review
GROUP BY CID;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q2
SELECT c.CID,
    c.first_name || ' ' || c.last_name AS name,
    CASE
        WHEN COALESCE(t.total_reviews, 0) = 0
            THEN 'not helpful'
        WHEN COALESCE(h.helpful_count, 0)::FLOAT
            / t.total_reviews >= 0.8
            THEN 'very helpful'
        WHEN COALESCE(h.helpful_count, 0)::FLOAT
            / t.total_reviews >= 0.5
            THEN 'somewhat helpful'
        ELSE 'not helpful'
    END AS helpfulness_category
FROM Customer c
LEFT JOIN TotalReviewCount t ON c.CID = t.CID
LEFT JOIN HelpfulCount h ON c.CID = h.CID;