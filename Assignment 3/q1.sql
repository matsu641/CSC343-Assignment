SET search_path TO TicketSchema;

WITH venue_capacity AS (
    SELECT
        sec.venue_id,
        COUNT(*) AS total_seats
    FROM Section sec
    JOIN Seat s ON s.section_id = sec.section_id
    GROUP BY sec.venue_id
),
concert_sales AS (
    SELECT
        c.concert_id,
        COUNT(t.ticket_id) AS tickets_sold,
        COALESCE(SUM(csp.price), 0) AS total_value_sold
    FROM Concert c
    LEFT JOIN Ticket t ON t.concert_id = c.concert_id
    LEFT JOIN Seat s ON s.seat_id = t.seat_id
    LEFT JOIN ConcertSectionPrice csp
        ON csp.concert_id = c.concert_id
       AND csp.section_id = s.section_id
    GROUP BY c.concert_id
)
SELECT
    c.concert_name,
    c.start_at,
    v.venue_name,
    cs.tickets_sold,
    cs.total_value_sold,
    ROUND((100.0 * cs.tickets_sold) / vc.total_seats, 2) AS pct_venue_sold
FROM Concert c
JOIN Venue v ON v.venue_id = c.venue_id
JOIN concert_sales cs ON cs.concert_id = c.concert_id
JOIN venue_capacity vc ON vc.venue_id = c.venue_id
ORDER BY c.start_at;
