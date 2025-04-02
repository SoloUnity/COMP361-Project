import sqlite3
import os
from utils.paths import DATABASE, resource_path
import subprocess

os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

def setup_database():
    conn = sqlite3.connect(DATABASE)
    schema_path = resource_path('database/schema.sql')
    
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())

    cursor = conn.cursor()
    
    # Insert the key "key" if no key exists
    cursor.execute("SELECT COUNT(*) FROM LicenseKey")
    count = cursor.fetchone()[0]
    
    if count == 0:  # Insert only if the table is empty
        cursor.execute(
            "INSERT INTO LicenseKey (key, verifiedOn) VALUES (?, datetime('now'))",
            ("key",)
        )
    
    conn.commit()
    conn.close()


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