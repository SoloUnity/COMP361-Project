import uuid
from datetime import datetime
from database.db import get_connection
import sqlite3

class Project:
    def __init__(self, project_id=None, created_on=None, last_saved_on=None,
                 top_left_x=0.0, top_left_y=0.0, bottom_right_x=100.0, bottom_right_y=100.0):
        self.project_id = project_id or str(uuid.uuid4())
        self.created_on = created_on or datetime.now()
        self.last_saved_on = last_saved_on or self.created_on
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y
    
    def get_bounding_box(self):
        return ((self.top_left_x, self.top_left_y), (self.bottom_right_x, self.bottom_right_y))
    
    def set_bounding_box(self, box):
        (self.top_left_x, self.top_left_y), (self.bottom_right_x, self.bottom_right_y) = box
    
    # Add property accessor for boundingBox
    @property
    def boundingBox(self):
        """Return the bounding box as a tuple of tuples: ((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))"""
        return self.get_bounding_box()
    
    @boundingBox.setter
    def boundingBox(self, box):
        """Set the bounding box from a tuple of tuples: ((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))"""
        self.set_bounding_box(box)

def get_project_by_id(project_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Project WHERE ProjectID = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Project(
            project_id=row["ProjectID"], 
            created_on=row["CreatedOn"], 
            last_saved_on=row["LastSavedOn"],
            top_left_x=row["TopLeftX"],
            top_left_y=row["TopLeftY"],
            bottom_right_x=row["BottomRightX"],
            bottom_right_y=row["BottomRightY"]
        )
    return None

def create_project():
    project = Project()
    
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO Project 
               (ProjectID, CreatedOn, LastSavedOn, TopLeftX, TopLeftY, BottomRightX, BottomRightY) 
               VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (
        project.project_id,
        project.created_on,
        project.last_saved_on,
        project.top_left_x,
        project.top_left_y,
        project.bottom_right_x,
        project.bottom_right_y
    ))
    conn.commit()
    conn.close()
    
    return project

def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Project WHERE ProjectID = ?"
    cursor.execute(query, (project_id,))
    rows_deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_deleted > 0