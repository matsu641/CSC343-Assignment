-- Could not:
-- 1) Enforce that Ticket.seat_id must belong to the same venue as
--    Ticket.concert_id without assertions or triggers.
-- 2) Enforce that ConcertSectionPrice.section_id must belong to the same venue
--    as ConcertSectionPrice.concert_id without assertions or triggers.
--
-- Did not:
-- None.
--
-- Extra constraints:
-- 1) Venue has a UNIQUE(city, street_address) constraint.
-- 2) Ticket has UNIQUE(concert_id, seat_id) to prevent double-selling a seat.
-- 3) ConcertSectionPrice has UNIQUE(concert_id, section_id).
--
-- Assumptions:
-- 1) A ticket is for one concrete seat at one concert.
-- 2) A purchase may include multiple tickets.
-- 3) A venue's section layout is fixed across all concerts in that venue.

DROP SCHEMA IF EXISTS TicketSchema CASCADE;
CREATE SCHEMA TicketSchema;
SET search_path TO TicketSchema;

-- A row means one owner (person/company) with a unique phone number.
CREATE TABLE Owner (
    owner_id SERIAL PRIMARY KEY,
    owner_name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);

-- A row means one venue at one city/street address with exactly one owner.
CREATE TABLE Venue (
    venue_id SERIAL PRIMARY KEY,
    venue_name TEXT NOT NULL,
    city TEXT NOT NULL,
    street_address TEXT NOT NULL,
    owner_id INTEGER NOT NULL REFERENCES Owner(owner_id),
    UNIQUE (city, street_address)
);

-- A row means one named section in one venue.
CREATE TABLE Section (
    section_id SERIAL PRIMARY KEY,
    venue_id INTEGER NOT NULL REFERENCES Venue(venue_id),
    section_name TEXT NOT NULL,
    UNIQUE (venue_id, section_name)
);

-- A row means one physical seat in one section of one venue.
CREATE TABLE Seat (
    seat_id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES Section(section_id),
    seat_name TEXT NOT NULL,
    is_accessible BOOLEAN NOT NULL,
    UNIQUE (section_id, seat_name)
);

-- A row means one concert at one venue and start timestamp.
CREATE TABLE Concert (
    concert_id SERIAL PRIMARY KEY,
    concert_name TEXT NOT NULL,
    start_at TIMESTAMP NOT NULL,
    venue_id INTEGER NOT NULL REFERENCES Venue(venue_id),
    UNIQUE (venue_id, start_at)
);

-- A row means one section price for one concert.
CREATE TABLE ConcertSectionPrice (
    concert_section_price_id SERIAL PRIMARY KEY,
    concert_id INTEGER NOT NULL REFERENCES Concert(concert_id),
    section_id INTEGER NOT NULL REFERENCES Section(section_id),
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    UNIQUE (concert_id, section_id)
);

-- A row means one app user identified by a unique username.
CREATE TABLE AppUser (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE
);

-- A row means one purchase event made by one user at one time.
CREATE TABLE Purchase (
    purchase_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES AppUser(user_id),
    purchased_at TIMESTAMP NOT NULL
);

-- A row means one sold ticket: one seat, one concert, one purchase record.
CREATE TABLE Ticket (
    ticket_id SERIAL PRIMARY KEY,
    purchase_id INTEGER NOT NULL REFERENCES Purchase(purchase_id),
    concert_id INTEGER NOT NULL REFERENCES Concert(concert_id),
    seat_id INTEGER NOT NULL REFERENCES Seat(seat_id),
    UNIQUE (concert_id, seat_id)
);
