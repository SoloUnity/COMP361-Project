import uuid
from datetime import datetime
from database.db import  get_connection
import sqlite3

class Project:
    def __init__(self, project_id=None, created_on=None, last_saved_on=None):
        self.project_id = project_id or str(uuid.uuid4())
        self.created_on = created_on or datetime.now()
        self.last_saved_on = last_saved_on or self.created_on

def get_project_by_id(project_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Project WHERE ProjectID = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Project(project_id=row["ProjectID"], created_on=row["CreatedOn"], last_saved_on=row["LastSavedOn"])
    return None