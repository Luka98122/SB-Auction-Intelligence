import mysql.connector
import os
import time

def connect_to_db():
    # Fetch credentials from environment variables
    db_config = {
        'host': os.getenv("DB_HOST", "db"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'database': os.getenv("DB_NAME")
    }

    while True:
        try:
            print("Attempting to connect to the MySQL database...")
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                print("Successfully connected to the database.")
                return conn
        except mysql.connector.Error as err:
            print(f"Database not ready yet: {err}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    db = connect_to_db()
    
    # Simple test query to prove it works
    cursor = db.cursor()
    cursor.execute("SHOW TABLES;")
    print(f"Existing tables: {cursor.fetchall()}")
    
    cursor.close()
    db.close()