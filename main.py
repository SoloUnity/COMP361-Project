from gui.gui import Program
from database.db import setup_database

def main():
    # Setup database
    setup_database()

    # Start GUI
    program = Program()
    program.run()

if __name__ == "__main__":
    main()