import sqlite3
import os
from utils.paths import DATABASE, resource_path

os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

def setup_database():
    conn = sqlite3.connect(DATABASE)
    schema_path = resource_path('database/schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DATABASE)