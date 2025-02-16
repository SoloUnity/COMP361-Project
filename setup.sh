#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "🔍 Checking required dependencies..."

# Step 1: Check if Docker is installed
if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Step 2: Check if Docker Compose is installed
if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Step 3: Check if MySQL Python Connector is installed
if ! python3 -c "import mysql.connector" 2>/dev/null; then
    echo "❌ MySQL Connector for Python is not installed. Installing it now..."
    pip install mysql-connector-python
fi

# Step 4: Check if Docker daemon is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker daemon is not running. Please start Docker and try again."
    exit 1
fi

# Step 5: Check if the MySQL container exists
if docker ps -a --format '{{.Names}}' | grep -q '^mars_mysql$'; then
    echo "✅ MySQL container exists."
else
    echo "🚀 MySQL container does not exist. Starting it now..."
    docker-compose up -d
fi

# Step 6: Wait for MySQL to start
echo "⏳ Waiting for MySQL to be ready..."
while ! docker exec mars_mysql mysqladmin ping -h"localhost" --silent > /dev/null 2>&1; do
    sleep 2
done

echo "✅ MySQL is ready!"

# Step 7: Log into MySQL interactively
echo "🔑 Logging into MySQL as user..."
docker exec -it mars_mysql mysql -u user -p'password' -D mars_rover_sim