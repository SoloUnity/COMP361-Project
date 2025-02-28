#Place holder 

import csv

# Hard-coded csv
FILENAME = 'gui/license_keys.csv' 

class KeyVerifier:
    def __init__(self):
        # Load license keys from the hard-coded file
        self.license_keys = self.load_license_keys(FILENAME)

    @staticmethod
    def load_license_keys(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            return {row[0] for row in reader}

    @staticmethod
    def check_license_key(license_keys, key_to_check):
        return key_to_check in license_keys
    
    def verify_license_key(self, key_to_check):
        return self.check_license_key(self.license_keys, key_to_check)

