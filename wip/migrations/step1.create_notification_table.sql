CREATE TABLE notification (
    enabled BOOLEAN NOT NULL DEFAULT false,
    subject VARCHAR(100) NOT NULL DEFAULT "Food items about to expire",
    to_addr VARCHAR(50) NOT NULL DEFAULT "e.mail@example.com",
    days INTEGER NOT NULL DEFAULT 3,
    time VARCHAR(5) NOT NULL DEFAULT "12:00"
);

INSERT INTO notification (enabled) VALUES (false);
