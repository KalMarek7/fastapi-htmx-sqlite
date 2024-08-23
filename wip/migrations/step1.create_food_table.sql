CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    expiry_date DATETIME NOT NULL,
    image TEXT,
    category VARCHAR(100) NOT NULL,
    notes TEXT
);
