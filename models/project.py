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

        self.bounding_box = None 
        self.selecting_box = False
        self.selection_made = False
        self.start_pos = None
        self.bounding_box_selected = False
        self.relative_bounding_box = None
    
    def get_bounding_box(self):
        return ((self.top_left_x, self.top_left_y), (self.bottom_right_x, self.bottom_right_y))
    
    def set_bounding_box(self, box):
        (self.top_left_x, self.top_left_y), (self.bottom_right_x, self.bottom_right_y) = box
    
    @property
    def boundingBox(self):
        return self.get_bounding_box()
    
    @boundingBox.setter
    def boundingBox(self, box):
        self.set_bounding_box(box)

    def start_selection(self, coords):
        self.start_pos = coords
        self.selecting_box = True
    
    def update_selection(self, coords):
        if self.selecting_box:
            self.bounding_box = (
                self.start_pos[0],
                self.start_pos[1],
                coords[0],
                coords[1]
            )
        
    def finalize_selection(self):
        if self.bounding_box:
            self.bounding_box_selected = True
            self.selection_made = False
            self.top_left_x = min(self.bounding_box[0], self.bounding_box[2])
            self.top_left_y = min(self.bounding_box[1], self.bounding_box[3])
            self.bottom_right_x = max(self.bounding_box[0], self.bounding_box[2])
            self.bottom_right_y = max(self.bounding_box[1], self.bounding_box[3])

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

def update_project(project):
    conn = get_connection()
    cursor = conn.cursor()
    query = """UPDATE Project 
              SET LastSavedOn = ?, TopLeftX = ?, TopLeftY = ?, 
                  BottomRightX = ?, BottomRightY = ? 
              WHERE ProjectID = ?"""
    cursor.execute(query, (
        datetime.now(),
        project.top_left_x,
        project.top_left_y,
        project.bottom_right_x,
        project.bottom_right_y,
        project.project_id
    ))
    rows_updated = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_updated > 0

def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Project WHERE ProjectID = ?"
    cursor.execute(query, (project_id,))
    rows_deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_deleted > 0