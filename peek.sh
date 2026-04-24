#!/bin/bash

# Load variables from .env
export $(grep -v '^#' .env | xargs)

# Set defaults
LIMIT=${1:-15} # Default to 15 if $1 is empty
SORT_BY="end_time DESC"

# Check for random flag
if [[ "$2" == "rand" || "$2" == "random" ]]; then
    SORT_BY="RAND()"
    echo "--- Sampling $LIMIT random items ---"
else
    echo "--- Showing latest $LIMIT items ---"
fi

QUERY="SELECT 
    final_price, 
    RIGHT(buyer_uuid, 16) AS buyer_tail, 
    LENGTH(item_bytes) AS bytes_len, 
    RIGHT(auction_uuid, 10) AS auction_tail 
FROM auctions 
ORDER BY $SORT_BY 
LIMIT $LIMIT;"

docker exec -it skyblock_mysql mysql -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "$QUERY"