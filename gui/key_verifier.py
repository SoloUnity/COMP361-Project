from api.api import verify_license_key

class KeyVerifier:
    def __init__(self):
        pass
    
    def verify_license_key(self, key_to_check):
        return verify_license_key(key_to_check)