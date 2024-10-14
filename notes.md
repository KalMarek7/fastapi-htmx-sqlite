-- Pictures table for storing image information
CREATE TABLE pictures (
id INTEGER PRIMARY KEY AUTOINCREMENT,
src TEXT NOT NULL,
filename VARCHAR(50),
filesize INT
);

-- Items table for storing additional information about the picture
CREATE TABLE items (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(255) NOT NULL,
expiry_date DATETIME NOT NULL,
picture_id INTEGER, -- Foreign key to the pictures table
category VARCHAR(100) NOT NULL,
notes TEXT,
FOREIGN KEY (picture_id) REFERENCES pictures(id) -- Foreign key constraint
);

```

return cur.lastrowid # Get the id of the inserted row


https://daisyui.com/components/navbar/
https://daisyui.com/components/file-input/
```
