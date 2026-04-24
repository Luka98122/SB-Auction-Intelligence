#!/bin/bash

# Load variables from .env
export $(grep -v '^#' .env | xargs)

echo "--- SB-Auction-Intelligence: Storage Report ---"

docker exec -it skyblock_mysql mysql -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "
SELECT 
    (SELECT COUNT(*) FROM auctions) AS 'Total Row Count',
    table_name AS 'Table Name', 
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)' 
FROM information_schema.TABLES 
WHERE table_schema = '$MYSQL_DATABASE' AND table_name = 'auctions';"