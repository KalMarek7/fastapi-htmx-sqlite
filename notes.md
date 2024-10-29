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
https://merakiui.com/components/application-ui/cards
```

-   [x] Ability to edit items (add close button and patch to a form)
-   [x] Conditionally render expiry date's color
-   [x] Handle image upload success somehow instead of message: success
-   Maybe add proper form on upload image so no edit image is required?
-   [x] (use existing "/api/v1/date_filtered_items" endpoint through cron job?) Recurring scan of items to send an email with items about to expire
-   [x] Refactor endpoints (https://dev.to/msnmongare/best-practices-for-naming-api-endpoints-2n5o?ref=dailydev)
-   Install tailwind and style UI from scratch
-   [x] Secure api key header for all requests as access restriction measure
