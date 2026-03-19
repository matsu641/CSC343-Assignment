SET search_path TO TicketSchema;

WITH user_ticket_counts AS (
    SELECT
        u.username,
        COUNT(t.ticket_id) AS ticket_count
    FROM AppUser u
    JOIN Purchase p ON p.user_id = u.user_id
    JOIN Ticket t ON t.purchase_id = p.purchase_id
    GROUP BY u.user_id, u.username
)
SELECT
    utc.username,
    utc.ticket_count
FROM user_ticket_counts utc
WHERE utc.ticket_count = (
    SELECT MAX(ticket_count) FROM user_ticket_counts
)
ORDER BY utc.username;
