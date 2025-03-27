import sqlite3
import os
from utils.paths import DATABASE, resource_path
import subprocess
import re

os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

def setup_database():
    db_exists = os.path.exists(DATABASE)
    
    if db_exists:
        if has_schema_changed():
            print(f"Schema changes detected. Backing up database...")
            backup_database()
            recreate_database()
        else:
            print(f"Database schema is up to date.")
    else:
        create_new_database()

def has_schema_changed():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
    
    schema_path = resource_path('database/schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    expected_tables = []
    for create_stmt in schema_sql.split("CREATE TABLE IF NOT EXISTS"):
        if not create_stmt.strip():
            continue
        table_name = create_stmt.strip().split("(")[0].strip()
        if table_name:
            expected_tables.append(table_name)
    
    if len(tables) != len(expected_tables):
        conn.close()
        return True
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        table_pattern = f"CREATE TABLE IF NOT EXISTS {table}"
        if table_pattern not in schema_sql:
            conn.close()
            return True
            
        table_schema = schema_sql.split(table_pattern)[1].split(");")[0]
        expected_column_count = len(re.findall(r'[A-Za-z0-9_]+\s+[A-Za-z0-9_]+', table_schema))
        
        if len(columns) != expected_column_count:
            conn.close()
            return True
    
    conn.close()
    return False

def backup_database():
    import shutil
    from datetime import datetime
    
    backup_dir = os.path.dirname(DATABASE)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"spacey_db_backup_{timestamp}.db")
    
    try:
        conn = get_connection()
        conn.close()
    except:
        pass
    
    shutil.copy2(DATABASE, backup_path)
    print(f"Database backed up to {backup_path}")

def recreate_database():
    try:
        os.remove(DATABASE)
    except:
        pass
    
    create_new_database()

def create_new_database():
    conn = sqlite3.connect(DATABASE)
    schema_path = resource_path('database/schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print(f"New database created successfully.")

def get_connection():
    return sqlite3.connect(DATABASE)

def clear_license_keys():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LicenseKey")
        rows_deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rows_deleted == 0:
            try:
                result = subprocess.run(
                    f'sqlite3 {DATABASE} "DELETE FROM LicenseKey;"',
                    shell=True, 
                    capture_output=True, 
                    text=True
                )
                if result.returncode != 0:
                    print(f"Failed: {result.stderr}")
            except Exception as e:
                print(f"Failed: {e}")
    except Exception as e:
        print(f"Failed: {e}")