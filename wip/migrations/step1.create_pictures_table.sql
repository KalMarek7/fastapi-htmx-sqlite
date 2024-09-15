CREATE TABLE pictures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    src TEXT NOT NULL,
    filename VARCHAR(55) NOT NULL,
    filesize INT NOT NULL,
    initial BOOLEAN NOT NULL
);