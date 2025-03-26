import uuid
import sqlite3
from datetime import datetime
from database.db import get_connection

class Rover:
    def __init__(self, rover_id=None, name='', weight=0.0, yearLaunched=None, status='Healthy', 
                 manufacturer='', top_speed=0.0, wheel_count=0, max_incline=0.0, last_trajectory=None, 
                 sprite_file_path='', total_distance_traveled=0.0, power_source='', description='',
                 lowSlopeEnergy=0.0, midSlopeEnergy=0.0, highSlopeEnergy=0.0):
        self.rover_id = rover_id or str(uuid.uuid4())
        self.name = name
        self.weight = weight
        self.yearLaunched = yearLaunched or datetime.now().year
        self.status = status
        self.manufacturer = manufacturer
        self.top_speed = top_speed
        self.wheel_count = wheel_count
        self.max_incline = max_incline
        self.last_trajectory = last_trajectory
        self.sprite_file_path = sprite_file_path
        self.total_distance_traveled = total_distance_traveled
        self.power_source = power_source
        self.description = description
        self.lowSlopeEnergy = lowSlopeEnergy
        self.midSlopeEnergy = midSlopeEnergy
        self.highSlopeEnergy = highSlopeEnergy

def get_rover_by_id(rover_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Rover WHERE RoverID = ?", (rover_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Rover(
            rover_id=row["RoverID"],
            name=row["Name"],
            weight=row["Weight"],
            yearLaunched=row["yearLaunched"],
            status=row["Status"],
            manufacturer=row["Manufacturer"],
            top_speed=row["topSpeed"],
            wheel_count=row["wheelCount"],
            max_incline=row["maxIncline"],
            last_trajectory=row["lastTrajectory"],
            sprite_file_path=row["spriteFilePath"],
            total_distance_traveled=row["totalDistanceTraveled"],
            power_source=row["powerSource"],
            description=row["description"],
            lowSlopeEnergy=row["lowSlopeEnergy"],
            midSlopeEnergy=row["midSlopeEnergy"],
            highSlopeEnergy=row["highSlopeEnergy"]
        )
    return None

# This needs to be here to prevent circular importing. Please don't remove.
from models.presets import create_curiosity, create_perseverance, create_lunokhod1, create_lunokhod2

def create_rover(rover_type):
    r = rover_type.lower()
    if r == "curiosity":
        rover = create_curiosity()
    elif r == "perseverance":
        rover = create_perseverance()
    elif r == "lunokhod1":
        rover = create_lunokhod1()
    elif r == "lunokhod2":
        rover = create_lunokhod2()
    else:
        raise ValueError("Unknown rover type: " + rover_type)

    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO Rover 
               (RoverID, Name, Weight, yearLaunched, Status, Manufacturer, topSpeed, 
                wheelCount, maxIncline, lastTrajectory, spriteFilePath, 
                totalDistanceTraveled, powerSource, description,
                lowSlopeEnergy, midSlopeEnergy, highSlopeEnergy) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (
        rover.rover_id, rover.name, rover.weight, rover.yearLaunched,
        rover.status, rover.manufacturer, rover.top_speed,
        rover.wheel_count, rover.max_incline, rover.last_trajectory,
        rover.sprite_file_path, rover.total_distance_traveled, 
        rover.power_source, rover.description,
        rover.lowSlopeEnergy, rover.midSlopeEnergy, rover.highSlopeEnergy
    ))
    conn.commit()
    conn.close()
    
    return rover

def delete_rover(rover_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Rover WHERE RoverID = ?"
    cursor.execute(query, (rover_id,))
    rows_deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_deleted > 0