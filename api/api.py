from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://spacey:OcxbDZfgYt1cny7S@cluster0.vdl1l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

def verify_license_key(key):
    try:
        db = client["LicenseKeys"]
        key_collection = db["key"]
        
        result = key_collection.find_one({"key": key})
        
        return result is not None
        
    except Exception as e:
        print(f"Error verifying license key: {e}")
        return False