#!/bin/bash

# Stop any currently running containers
docker compose down

# Rebuild and start the services
echo "Rebuilding and starting SB-Auction-Intelligence..."
docker compose up --build