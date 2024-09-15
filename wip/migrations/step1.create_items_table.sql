CREATE TABLE items (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(255) NOT NULL,
expiry_date VARCHAR(50) NOT NULL,
picture_id INTEGER, -- Foreign key to the pictures table
category VARCHAR(100),
notes TEXT,
FOREIGN KEY (picture_id) REFERENCES pictures(id) -- Foreign key constraint
)