import sqlite3
from datetime import datetime
from database.db import get_connection
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://spacey:OcxbDZfgYt1cny7S@cluster0.vdl1l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

def verify_license_key(key):
    saved_key = get_saved_key()
    if saved_key and saved_key == key:
        return True
        
    try:
        db = client["LicenseKeys"]
        key_collection = db["key"]
        result = key_collection.find_one({"key": key})
        is_valid = result is not None
        
        if is_valid:
            save_key(key)
            
        return is_valid
    except Exception as e:
        print(f"Error verifying license key: {e}")
        return False

def get_saved_key():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key FROM LicenseKey ORDER BY verifiedOn DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None
    except Exception as e:
        print(f"Error retrieving saved license key: {e}")
        return None

def save_key(key):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        current_time = datetime.now()
        cursor.execute("INSERT INTO LicenseKey (key, verifiedOn) VALUES (?, ?)", 
                      (key, current_time))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving license key: {e}")

def has_valid_key():
    return get_saved_key() is not None