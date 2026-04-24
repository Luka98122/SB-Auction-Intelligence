#!/bin/bash

# Define the image name (Docker typically uses the folder name as a prefix)
IMAGE_NAME="sb-auction-intelligence-scraper"

# Check if the image exists and get its creation time
LAST_BUILD=$(docker inspect -f '{{.Created}}' $IMAGE_NAME:latest 2>/dev/null)

if [ $? -eq 0 ]; then
    # Format the ISO timestamp into something more readable
    READABLE_TIME=$(date -d "$LAST_BUILD" "+%Y-%m-%d %H:%M:%S")
    echo "Last build of $IMAGE_NAME was: $READABLE_TIME"
    echo "Starting stack..."
    nohup docker compose up
else
    echo "Error: No existing build found for $IMAGE_NAME."
    echo "Run ./build.sh first to create the image."
    exit 1
fi