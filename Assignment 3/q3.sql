SET search_path TO TicketSchema;

SELECT
    v.venue_name,
    COUNT(s.seat_id) AS seat_count,
    ROUND(
        100.0 * AVG(CASE WHEN s.is_accessible THEN 1.0 ELSE 0.0 END),
        2
    ) AS pct_accessible
FROM Venue v
JOIN Section sec ON sec.venue_id = v.venue_id
JOIN Seat s ON s.section_id = sec.section_id
GROUP BY v.venue_id, v.venue_name
ORDER BY v.venue_name;
