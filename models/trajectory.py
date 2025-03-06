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

def create_trajectory(rover_id, project_id, current_coord, target_coord, coordinate_list=None, total_distance=0.0):
    trajectory = Trajectory(
        rover_id=rover_id,
        project_id=project_id,
        current_coord=current_coord,
        target_coord=target_coord,
        coordinate_list=coordinate_list,
        total_distance=total_distance
    )
    coord_list_str = str(trajectory.coordinate_list) if trajectory.coordinate_list else "[]"
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO Trajectory 
              (TrajectoryID, RoverID, ProjectID, currentCoord, targetCoord, startTime, 
               endTime, coordinateList, totalDistance, distanceTraveled) 
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (
        trajectory.trajectory_id,
        trajectory.rover_id,
        trajectory.project_id,
        trajectory.current_coord,
        trajectory.target_coord,
        trajectory.start_time,
        trajectory.end_time,
        coord_list_str,
        trajectory.total_distance,
        trajectory.distance_traveled
    ))
    conn.commit()
    conn.close()
    
    return trajectory

def delete_trajectory(trajectory_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Trajectory WHERE TrajectoryID = ?"
    cursor.execute(query, (trajectory_id,))
    rows_deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_deleted > 0