import os
import mysql.connector

# Fetch credentials from the environment variables set in docker-compose.yml
db_connection = mysql.connector.connect(
    host=os.getenv("DB_HOST", "db"), # "db" matches the service name in docker-compose
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("Successfully connected to the database!")