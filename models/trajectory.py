import uuid
from datetime import datetime
from database.db import  get_connection
import sqlite3

class Trajectory:
    def __init__(self, trajectory_id=None, rover_id='', project_id='', current_coord='', target_coord='', start_time=None, end_time=None, coordinate_list=None, total_distance=0.0, distance_traveled=0.0):
        self.trajectory_id = trajectory_id or str(uuid.uuid4())
        self.rover_id = rover_id
        self.project_id = project_id
        self.current_coord = current_coord
        self.target_coord = target_coord
        self.start_time = start_time or datetime.now()
        self.end_time = end_time
        self.coordinate_list = coordinate_list or []
        self.total_distance = total_distance
        self.distance_traveled = distance_traveled

def get_trajectory_by_id(trajectory_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Trajectory WHERE TrajectoryID = ?", (trajectory_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Trajectory(
            trajectory_id=row["TrajectoryID"],
            rover_id=row["RoverID"],
            project_id=row["ProjectID"],
            current_coord=row["currentCoord"],
            target_coord=row["targetCoord"],
            start_time=row["startTime"],
            end_time=row["endTime"],
            coordinate_list=row["coordinateList"],
            total_distance=row["totalDistance"],
            distance_traveled=row["distanceTraveled"]
        )
    return None