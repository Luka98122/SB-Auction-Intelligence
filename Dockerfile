# Use an official, lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code into the container
COPY scraper.py .

# Command to run your scraper
CMD ["python", "scraper.py"]