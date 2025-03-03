import sqlite3
import os
from utils.paths import DATABASE, resource_path

os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

def setup_database():
    """Initialize the SQLite database with schema"""
    conn = sqlite3.connect(DATABASE)
    
    schema_path = resource_path('database/schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()

def get_connection():
    """Get a connection to the SQLite database"""
    return sqlite3.connect(DATABASE)

def fetch_rovers():
    """Fetch all rovers from the database"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Rover")
    rovers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rovers

def fetch_trajectory(rover_id):
    """Fetch trajectory for a specific rover"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Trajectory WHERE RoverID = ?", (rover_id,))
    trajectory = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return trajectory

def add_rover(rover_data):
    """Add a new rover to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    columns = ', '.join(rover_data.keys())
    placeholders = ', '.join(['?'] * len(rover_data))
    values = tuple(rover_data.values())
    
    query = f"INSERT INTO Rover ({columns}) VALUES ({placeholders})"
    cursor.execute(query, values)
    
    conn.commit()
    conn.close()
    return cursor.lastrowid

def update_rover(rover_id, rover_data):
    """Update rover information"""
    conn = get_connection()
    cursor = conn.cursor()
    
    set_clause = ', '.join([f"{key} = ?" for key in rover_data.keys()])
    values = list(rover_data.values()) + [rover_id]
    
    query = f"UPDATE Rover SET {set_clause} WHERE RoverID = ?"
    cursor.execute(query, values)
    
    conn.commit()
    conn.close()
    return cursor.rowcount

def add_trajectory(trajectory_data):
    """Add a new trajectory entry"""
    conn = get_connection()
    cursor = conn.cursor()
    
    columns = ', '.join(trajectory_data.keys())
    placeholders = ', '.join(['?'] * len(trajectory_data))
    values = tuple(trajectory_data.values())
    
    query = f"INSERT INTO Trajectory ({columns}) VALUES ({placeholders})"
    cursor.execute(query, values)
    
    conn.commit()
    conn.close()
    return cursor.lastrowid