CREATE TABLE IF NOT EXISTS auctions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    auction_uuid VARCHAR(64) UNIQUE,
    item_name VARCHAR(255),
    tier VARCHAR(50),
    category VARCHAR(50),
    starting_bid BIGINT,
    bin BOOLEAN, -- Buy It Now
    end_time DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_item_name ON auctions(item_name);