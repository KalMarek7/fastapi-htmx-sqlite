CREATE TABLE notification (
    enabled BOOLEAN NOT NULL DEFAULT false,
    subject VARCHAR(100) NOT NULL DEFAULT "Food items about to expire",
    to_addr VARCHAR(50) NOT NULL DEFAULT "e.mail@example.com"
);

INSERT INTO notification (enabled) VALUES (false);
