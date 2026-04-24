import requests
import mysql.connector
import os
import time
from datetime import datetime

# Handy one liner to check the highest buyers:
# export $(grep -v '^#' .env | xargs) && docker exec -it skyblock_mysql mysql -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE -e "SELECT buyer_uuid, COUNT(*) AS count FROM auctions GROUP BY buyer_uuid ORDER BY count DESC LIMIT 3;"

#Check the number of auctions collected:
# docker exec -it skyblock_mysql mysql -u luka_dev -p skyblock_data -e "SELECT COUNT(*) FROM auctions;"

# --- Database Connection ---
def get_db_connection():
    while True:
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except mysql.connector.Error as err:
            print(f"Database not ready: {err}. Retrying in 5s...")
            time.sleep(5)

# --- Main Polling Loop ---
def run_scraper():
    db = get_db_connection()
    cursor = db.cursor()
    ended_url = "https://api.hypixel.net/v2/skyblock/auctions_ended"

    # INSERT IGNORE safely handles overlap between 60-second polling windows
    insert_query = """
    INSERT IGNORE INTO auctions (auction_uuid, seller_uuid, buyer_uuid, final_price, bin, end_time, item_bytes)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    print("SB-Auction-Intelligence: Raw ELT Pipeline Started.")

    while True:
        try:
            start_time = time.time()
            response = requests.get(ended_url, timeout=10).json()
            
            if not response.get("success"):
                print("API request failed, retrying...")
                time.sleep(10)
                continue

            ended_auctions = response.get("auctions", [])
            data_tuples = []

            for a in ended_auctions:
                # We only care about items that actually sold
                if 'buyer' not in a: 
                    continue 
                
                end_dt = datetime.fromtimestamp(a['timestamp'] / 1000.0)
                
                data_tuples.append((
                    a['auction_id'],
                    a['seller'],
                    a['buyer'],
                    a['price'],
                    a.get('bin', False),
                    end_dt,
                    a['item_bytes']  # Storing the raw Base64 payload directly
                ))

            if data_tuples:
                # Batch insert for high-speed I/O
                cursor.executemany(insert_query, data_tuples)
                db.commit()

            # The ended API updates roughly every 60 seconds.
            elapsed = time.time() - start_time
            sleep_time = max(0, 60 - elapsed)
            
            print(f"Logged {len(data_tuples)} raw sales. Sleeping for {round(sleep_time)}s...")
            time.sleep(sleep_time)

        except Exception as e:
            print(f"Error in polling loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_scraper()