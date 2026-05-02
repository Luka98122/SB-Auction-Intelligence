# SB-Auction-Intelligence

An integrated data engineering and machine learning pipeline designed to ingest, process, and analyze Hypixel Skyblock auction data. This project automates the transition from raw API responses to structured datasets suitable for deep learning and predictive modeling. The dataset created for this project can be found [here](https://www.kaggle.com/datasets/luka98122/hypixel-skyblock-bin-auctions/data).

---

## Project Overview

**SB-Auction-Intelligence** is a containerized ecosystem built to handle the full lifecycle of market data. It moves beyond simple scraping by providing a scalable infrastructure to store historical price points and engineer features for machine learning models.

The system is composed of three primary layers:
* **Ingestion:** A Python-based scraper that polls the Hypixel API for active and recently ended auctions.
* **Persistence:** A Dockerized MySQL instance optimized for time-series market data.
* **Analysis:** A processing suite for cleaning data and training ML models to identify market inefficiencies and price trends.

---

## Infrastructure and Requirements

This project relies on Docker and Docker Compose to ensure environment parity across different systems. By containerizing the stack, the Python scraper and MySQL database are isolated from the host machine while maintaining a high-speed internal network.

### Prerequisites
* Docker Engine and Docker Compose (Plugin)
* Python 3.11 (Development environment)
* A valid Hypixel API Key

---

## Project Structure

The repository is organized to separate infrastructure configuration from the data science logic.

```text
SB-Auction-Intelligence/
├── scripts/
│   └── init.sql          # SQL schema for the initial database setup
├── src/
│   ├── scraper.py        # Main API polling and ingestion logic
│   ├── processing/       # Feature engineering and data cleaning
│   └── models/           # ML model definitions and training loops
├── .env.example          # Template for environment variables
├── docker-compose.yml    # Orchestration of the Python and MySQL services
├── Dockerfile            # Blueprint for the Python environment
└── requirements.txt      # Python library dependencies
