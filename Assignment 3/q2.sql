SET search_path TO TicketSchema;

SELECT
    o.owner_name,
    COUNT(v.venue_id) AS venue_count
FROM Owner o
LEFT JOIN Venue v ON v.owner_id = o.owner_id
GROUP BY o.owner_id, o.owner_name
ORDER BY venue_count DESC, o.owner_name;
