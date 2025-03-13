import sys
from gui.gui import Program
from database.db import setup_database, clear_license_keys
from utils.paths import DATABASE

def main():
    if "--no-key" in sys.argv:
        clear_license_keys()
    
    # Setup database
    setup_database()

    # Start GUI
    program = Program()
    program.run()

if __name__ == "__main__":
    main()