CREATE TABLE IF NOT EXISTS auctions (
    auction_uuid VARCHAR(64) PRIMARY KEY,
    seller_uuid VARCHAR(64),
    buyer_uuid VARCHAR(64),
    final_price BIGINT,
    bin BOOLEAN,
    end_time DATETIME,
    item_bytes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- We index end_time so you can easily pull data in chronological batches later
CREATE INDEX idx_end_time ON auctions(end_time);