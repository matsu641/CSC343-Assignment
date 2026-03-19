SET search_path TO TicketSchema;

INSERT INTO Owner (owner_id, owner_name, phone) VALUES
(1, 'Aurora Entertainment Group', '416-555-0101'),
(2, 'Maple City Operations', '416-555-0102'),
(3, 'North Stage Holdings', '416-555-0103'),
(4, 'Grand River Venues', '416-555-0104'),
(5, 'Skyline Event Corp', '416-555-0105'),
(6, 'Lakeshore Arts Co', '416-555-0106');

INSERT INTO Venue (
    venue_id, venue_name, city, street_address, owner_id
) VALUES
(1, 'Harbour Dome', 'Toronto', '100 Queens Quay E', 1),
(2, 'Maple Hall', 'Toronto', '250 King St W', 1),
(3, 'Rose Arena', 'Mississauga', '11 Centre Dr', 1),
(4, 'Pine Theatre', 'Ottawa', '89 Sparks St', 2),
(5, 'Riverfront Stage', 'Hamilton', '55 Bay St N', 2),
(6, 'Summit Live House', 'Waterloo', '9 University Ave', 3),
(7, 'Midtown Pavilion', 'London', '77 Richmond St', 4),
(8, 'Garden Sound Space', 'Kingston', '18 Princess St', 5),
(9, 'Crescent Auditorium', 'Windsor', '210 Ouellette Ave', 5),
(10, 'Canal Concert Hall', 'Ottawa', '20 Rideau St', 6);

INSERT INTO Section (section_id, venue_id, section_name)
SELECT
    (v.venue_id - 1) * 2 + x.pos AS section_id,
    v.venue_id,
    x.section_name
FROM Venue v
CROSS JOIN (
    VALUES (1, 'Floor'), (2, 'Balcony')
) AS x(pos, section_name)
ORDER BY v.venue_id, x.pos;

-- Venue 1 has 60 seats total (30 per section). Others have 10 total (5/section).
INSERT INTO Seat (section_id, seat_name, is_accessible)
SELECT
    s.section_id,
    CASE
        WHEN s.section_name = 'Floor' THEN 'F' || gs.n::TEXT
        ELSE 'B' || gs.n::TEXT
    END AS seat_name,
    CASE
        WHEN s.venue_id = 1 THEN gs.n <= 15
        WHEN s.venue_id IN (3, 7) THEN gs.n <= 3
        WHEN s.venue_id = 5 THEN gs.n <= 2
        ELSE gs.n = 1
    END AS is_accessible
FROM Section s
CROSS JOIN generate_series(1, 30) AS gs(n)
WHERE s.venue_id = 1 OR gs.n <= 5
ORDER BY s.section_id, gs.n;

INSERT INTO Concert (concert_id, concert_name, start_at, venue_id) VALUES
(1, 'City Lights Festival', '2026-05-10 20:00:00', 1),
(2, 'Acoustic Night', '2026-05-12 19:30:00', 2),
(3, 'Retro Rewind', '2026-05-14 20:30:00', 3),
(4, 'Jazz in Spring', '2026-05-16 19:00:00', 4);

INSERT INTO ConcertSectionPrice (concert_id, section_id, price)
SELECT
    c.concert_id,
    s.section_id,
    CASE
        WHEN s.section_name = 'Floor' THEN
            CASE c.concert_id
                WHEN 1 THEN 120.00
                WHEN 2 THEN 65.00
                WHEN 3 THEN 80.00
                ELSE 90.00
            END
        ELSE
            CASE c.concert_id
                WHEN 1 THEN 75.00
                WHEN 2 THEN 45.00
                WHEN 3 THEN 55.00
                ELSE 60.00
            END
    END AS price
FROM Concert c
JOIN Section s ON s.venue_id = c.venue_id;

INSERT INTO AppUser (user_id, username) VALUES
(1, 'powerbuyer'),
(2, 'musicfan22'),
(3, 'latecheckout'),
(4, 'firstrowdreams'),
(5, 'balconybeats'),
(6, 'weekendvibes'),
(7, 'ticketscout');

INSERT INTO Purchase (purchase_id, user_id, purchased_at) VALUES
(1, 1, '2026-03-01 10:00:00'),
(2, 2, '2026-03-01 10:05:00'),
(3, 3, '2026-03-01 10:10:00'),
(4, 4, '2026-03-01 10:15:00'),
(5, 5, '2026-03-02 11:00:00'),
(6, 6, '2026-03-02 11:10:00'),
(7, 7, '2026-03-02 11:20:00'),
(8, 1, '2026-03-03 12:00:00');

-- Concert 1: 55 tickets sold (>= 50). User 1 buys 30 of these.
WITH ranked AS (
    SELECT seat_id, ROW_NUMBER() OVER (ORDER BY seat_id) AS rn
    FROM Seat
    WHERE section_id IN (
        SELECT section_id FROM Section WHERE venue_id = 1
    )
)
INSERT INTO Ticket (purchase_id, concert_id, seat_id)
SELECT
    CASE
        WHEN rn <= 30 THEN 1
        WHEN rn <= 40 THEN 2
        WHEN rn <= 48 THEN 3
        ELSE 4
    END AS purchase_id,
    1 AS concert_id,
    seat_id
FROM ranked
WHERE rn <= 55;

-- Concert 3: 8 tickets sold (between 0 and 50).
WITH ranked AS (
    SELECT seat_id, ROW_NUMBER() OVER (ORDER BY seat_id) AS rn
    FROM Seat
    WHERE section_id IN (
        SELECT section_id FROM Section WHERE venue_id = 3
    )
)
INSERT INTO Ticket (purchase_id, concert_id, seat_id)
SELECT
    CASE
        WHEN rn <= 2 THEN 1
        WHEN rn <= 4 THEN 5
        WHEN rn <= 6 THEN 6
        ELSE 7
    END AS purchase_id,
    3 AS concert_id,
    seat_id
FROM ranked
WHERE rn <= 8;

-- Concert 4: 5 tickets sold.
WITH ranked AS (
    SELECT seat_id, ROW_NUMBER() OVER (ORDER BY seat_id) AS rn
    FROM Seat
    WHERE section_id IN (
        SELECT section_id FROM Section WHERE venue_id = 4
    )
)
INSERT INTO Ticket (purchase_id, concert_id, seat_id)
SELECT
    CASE
        WHEN rn <= 3 THEN 8
        ELSE 2
    END AS purchase_id,
    4 AS concert_id,
    seat_id
FROM ranked
WHERE rn <= 5;
