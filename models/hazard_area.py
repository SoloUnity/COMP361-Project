import uuid
import sqlite3
from datetime import datetime
from database.db import get_connection

class HazardArea:
    def __init__(self, hazard_id=None, name='', description='', 
                 x1=0.0, y1=0.0, x2=0.0, y2=0.0, x3=0.0, y3=0.0, x4=0.0, y4=0.0,
                 project_id=None, created_on=None):
        self.hazard_id = hazard_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.project_id = project_id
        self.created_on = created_on or datetime.now()
    
def create_hazard_area(name, description, x1, y1, x2, y2, x3, y3, x4, y4, project_id=None):
    hazard_area = HazardArea(
        name=name,
        description=description,
        x1=x1, y1=y1,
        x2=x2, y2=y2,
        x3=x3, y3=y3,
        x4=x4, y4=y4,
        project_id=project_id
    )
    
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO HazardArea 
              (HazardID, Name, Description, x1, y1, x2, y2, x3, y3, x4, y4, ProjectID, CreatedOn) 
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (
        hazard_area.hazard_id,
        hazard_area.name,
        hazard_area.description,
        hazard_area.x1,
        hazard_area.y1,
        hazard_area.x2,
        hazard_area.y2,
        hazard_area.x3,
        hazard_area.y3,
        hazard_area.x4,
        hazard_area.y4,
        hazard_area.project_id,
        hazard_area.created_on
    ))
    conn.commit()
    conn.close()
    
    return hazard_area

def delete_hazard_area(hazard_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM HazardArea WHERE HazardID = ?"
    cursor.execute(query, (hazard_id,))
    rows_deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_deleted > 0    

def get_hazard_areas_by_project(project_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HazardArea WHERE ProjectID = ?", (project_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [HazardArea(
        hazard_id=row["HazardID"],
        name=row["Name"],
        description=row["Description"],
        x1=row["x1"],
        y1=row["y1"],
        x2=row["x2"],
        y2=row["y2"],
        x3=row["x3"],
        y3=row["y3"],
        x4=row["x4"],
        y4=row["y4"],
        project_id=row["ProjectID"],
        created_on=row["CreatedOn"]
    ) for row in rows]
