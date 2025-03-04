import uuid
from datetime import datetime
from database.db import  get_connection
import sqlite3

class Rover:
    def __init__(self, rover_id=None, name='', dimensions='', weight=0.0, date_created=None, status='Healthy', manufacturer='', total_range=0.0, range_left=0.0, top_speed=0.0, wheel_count=0, wheel_diameter=0.0, max_incline=0.0, last_trajectory=None, sprite_file_path='', total_distance_traveled=0.0, total_capacity=0.0, power_source=''):
        self.rover_id = rover_id or str(uuid.uuid4())
        self.name = name
        self.dimensions = dimensions
        self.weight = weight
        self.date_created = date_created or datetime.now()
        self.status = status
        self.manufacturer = manufacturer
        self.total_range = total_range
        self.range_left = range_left
        self.top_speed = top_speed
        self.wheel_count = wheel_count
        self.wheel_diameter = wheel_diameter
        self.max_incline = max_incline
        self.last_trajectory = last_trajectory
        self.sprite_file_path = sprite_file_path
        self.total_distance_traveled = total_distance_traveled
        self.total_capacity = total_capacity
        self.power_source = power_source

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
            dimensions=row["Dimensions"],
            weight=row["Weight"],
            date_created=row["dateCreated"],
            status=row["Status"],
            manufacturer=row["Manufacturer"],
            total_range=row["totalRange"],
            range_left=row["rangeLeft"],
            top_speed=row["topSpeed"],
            wheel_count=row["wheelCount"],
            wheel_diameter=row["wheelDiameter"],
            max_incline=row["maxIncline"],
            last_trajectory=row["lastTrajectory"],
            sprite_file_path=row["spriteFilePath"],
            total_distance_traveled=row["totalDistanceTraveled"],
            total_capacity=row["totalCapacity"],
            power_source=row["powerSource"]
        )
    return None

def add_rover_to_db(rover):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Rover (RoverID, Name, Dimensions, Weight, dateCreated, Status, Manufacturer, totalRange, rangeLeft, topSpeed, wheelCount, wheelDiameter, maxIncline, lastTrajectory, spriteFilePath, totalDistanceTraveled, totalCapacity, powerSource) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (
        rover.rover_id, rover.name, rover.dimensions, rover.weight, rover.date_created,
        rover.status, rover.manufacturer, rover.total_range, rover.range_left, rover.top_speed,
        rover.wheel_count, rover.wheel_diameter, rover.max_incline, rover.last_trajectory,
        rover.sprite_file_path, rover.total_distance_traveled, rover.total_capacity, rover.power_source
    ))
    conn.commit()
    conn.close()