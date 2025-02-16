# MySQL connection settings
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "mars_rover_sim",
    "port": 3306
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)