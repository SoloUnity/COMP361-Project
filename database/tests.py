import sys
import os
import time
import sqlite3
from datetime import datetime

'''
To test, go to the project's root dir and run:
python3 -m tests.test_models
'''

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.rover import create_rover, get_rover_by_id, delete_rover
from models.project import create_project, get_project_by_id, delete_project
from models.trajectory import create_trajectory, get_trajectory_by_id, delete_trajectory
from models.hazard_area import create_hazard_area, get_all_hazard_areas, delete_hazard_area
import database.db as db

# Define a test database path
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test.db')

def test_get_connection():
    return sqlite3.connect(TEST_DB_PATH)

def setup_test_database():
    """Set up a clean test database from the schema."""
    print_info("Setting up test database...")
    
    # Remove any existing test database
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    # Create a fresh test database
    conn = sqlite3.connect(TEST_DB_PATH)
    
    # Read the schema file
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Execute the schema
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    
    print_success(f"Test database created at {TEST_DB_PATH}")

def teardown_test_database():
    """Remove the test database."""
    print_info("Cleaning up test database...")
    
    # Close all connections
    try:
        conn = test_get_connection()
        conn.close()
    except:
        pass
    
    # Remove the test database file
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
        print_success("Test database removed")

class Colors:
    """ANSI color codes for pretty output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}    {text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_object(obj, obj_type):
    print(f"{Colors.YELLOW}🔍 {obj_type} Details:{Colors.ENDC}")
    
    for attr, value in vars(obj).items():
        if isinstance(value, datetime):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
            
        print(f"   {Colors.BOLD}{attr}{Colors.ENDC}: {value}")

def test_rover():
    print_header("🤖 Testing Rover CRUD Operations")
    
    print_info("Creating new project for rover...")
    project = create_project()
    
    print_info("Creating Curiosity rover associated with the project...")
    rover = create_rover("curiosity", project.project_id)
    print_success(f"Created rover: {rover.name} (ID: {rover.rover_id})")
    
    print_object(rover, "Rover")
    
    print_info("Verifying energy consumption values...")
    if (hasattr(rover, 'lowSlopeEnergy') and hasattr(rover, 'midSlopeEnergy') 
        and hasattr(rover, 'highSlopeEnergy')):
        print_success(f"Energy consumption fields found: Low: {rover.lowSlopeEnergy}, Mid: {rover.midSlopeEnergy}, High: {rover.highSlopeEnergy}")
    else:
        print_error("Energy consumption fields not found in rover object!")
        return False
    
    print_info(f"Retrieving rover with ID: {rover.rover_id}...")
    retrieved_rover = get_rover_by_id(rover.rover_id)
    
    if retrieved_rover and retrieved_rover.rover_id == rover.rover_id:
        print_success(f"Successfully retrieved rover: {retrieved_rover.name}")
        print_object(retrieved_rover, "Retrieved Rover")
    else:
        print_error("Failed to retrieve rover!")
        return False
    
    print_info(f"Deleting rover with ID: {rover.rover_id}...")
    if delete_rover(rover.rover_id):
        print_success(f"Successfully deleted rover: {rover.name}")
    else:
        print_error("Failed to delete rover!")
        return False
    
    if get_rover_by_id(rover.rover_id) is None:
        print_success("Verified rover was deleted from database")
    else:
        print_error("Rover still exists in database after deletion!")
        return False

    print_info(f"Deleting project with ID: {project.project_id}...")
    delete_project(project.project_id)
    
    return True

def test_project():
    print_header("📋 Testing Project CRUD Operations")
    
    print_info("Creating new project...")
    project = create_project()
    print_success(f"Created project with ID: {project.project_id}")
    print_object(project, "Project")
    
    # Test the boundingBox property
    print_info("Testing boundingBox property...")
    initial_box = project.boundingBox
    if initial_box == ((project.top_left_x, project.top_left_y), (project.bottom_right_x, project.bottom_right_y)):
        print_success(f"BoundingBox property correctly returns: {initial_box}")
    else:
        print_error("BoundingBox property returned incorrect values!")
        return False
    
    # Test setting the boundingBox
    new_box = ((10.0, 15.0), (200.0, 250.0))
    project.boundingBox = new_box
    if project.top_left_x == 10.0 and project.top_left_y == 15.0 and project.bottom_right_x == 200.0 and project.bottom_right_y == 250.0:
        print_success(f"BoundingBox property correctly set new values: {new_box}")
    else:
        print_error("BoundingBox property failed to set new values!")
        return False
    
    print_info(f"Retrieving project with ID: {project.project_id}...")
    retrieved_project = get_project_by_id(project.project_id)
    
    if retrieved_project and retrieved_project.project_id == project.project_id:
        print_success(f"Successfully retrieved project with ID: {retrieved_project.project_id}")
        print_object(retrieved_project, "Retrieved Project")
    else:
        print_error("Failed to retrieve project!")
        return False
    
    print_info(f"Deleting project with ID: {project.project_id}...")
    if delete_project(project.project_id):
        print_success(f"Successfully deleted project")
    else:
        print_error("Failed to delete project!")
        return False
    
    if get_project_by_id(project.project_id) is None:
        print_success("Verified project was deleted from database")
    else:
        print_error("Project still exists in database after deletion!")
        return False
    
    return True

def test_trajectory():
    print_header("🛣️ Testing Trajectory CRUD Operations")
    
    # First, create a project and a rover associated with that project
    project = create_project()
    rover = create_rover("perseverance", project.project_id)
    
    print_info("Creating new trajectory...")
    current_coord = "10.5,20.3"
    target_coord = "15.8,22.1"
    coordinate_list = [[10.5, 20.3], [12.0, 21.0], [15.8, 22.1]]
    
    trajectory = create_trajectory(
        rover.rover_id, 
        current_coord, 
        target_coord,
        coordinate_list=coordinate_list,
        total_distance=8.75,
        algo="dijkstra",
        heuristics='{"weight": 1.5, "allow_diagonal": true}'
    )
    
    print_success(f"Created trajectory with ID: {trajectory.trajectory_id}")
    print_object(trajectory, "Trajectory")
    
    print_info(f"Retrieving trajectory with ID: {trajectory.trajectory_id}...")
    retrieved_trajectory = get_trajectory_by_id(trajectory.trajectory_id)
    
    if (retrieved_trajectory and retrieved_trajectory.trajectory_id == trajectory.trajectory_id):
        print_success("Successfully retrieved trajectory")
        print_object(retrieved_trajectory, "Retrieved Trajectory")
        
        if retrieved_trajectory.algo == "dijkstra" and "weight" in retrieved_trajectory.heuristics:
            print_success("Algorithm and heuristics data correctly retrieved")
        else:
            print_error("Algorithm or heuristics data not correctly retrieved!")
            delete_rover(rover.rover_id)
            delete_project(project.project_id)
            return False
    else:
        print_error("Failed to retrieve trajectory!")
        delete_rover(rover.rover_id)
        delete_project(project.project_id)
        return False
    
    print_info(f"Deleting trajectory with ID: {trajectory.trajectory_id}...")
    if delete_trajectory(trajectory.trajectory_id):
        print_success("Successfully deleted trajectory")
    else:
        print_error("Failed to delete trajectory!")
        delete_rover(rover.rover_id)
        delete_project(project.project_id)
        return False
    
    if get_trajectory_by_id(trajectory.trajectory_id) is None:
        print_success("Verified trajectory was deleted from database")
    else:
        print_error("Trajectory still exists in database after deletion!")
        delete_rover(rover.rover_id)
        delete_project(project.project_id)
        return False
    
    delete_rover(rover.rover_id)
    delete_project(project.project_id)
    
    return True

def test_hazard_area():
    print_header("⚠️ Testing Hazard Area CRUD Operations")
    
    print_info("Creating new hazard area...")
    hazard_area = create_hazard_area(
        name="Steep Cliff",
        description="Dangerous cliff area with loose rocks",
        x1=10.5, y1=20.3,
        x2=10.5, y2=25.7,
        x3=15.8, y3=25.7,
        x4=15.8, y4=20.3
    )
    
    print_success(f"Created hazard area with ID: {hazard_area.hazard_id}")
    print_object(hazard_area, "Hazard Area")

    print_info("Retrieving all hazard areas...")
    retrieved_hazards = get_all_hazard_areas()  # We removed project_id dependency
    
    if retrieved_hazards and len(retrieved_hazards) > 0:
        retrieved_hazard = retrieved_hazards[0]
        
        if retrieved_hazard.hazard_id == hazard_area.hazard_id:
            print_success(f"Successfully retrieved hazard area with ID: {retrieved_hazard.hazard_id}")
            print_object(retrieved_hazard, "Retrieved Hazard Area")
        else:
            print_error("Retrieved hazard area doesn't match the created one!")
            return False
    else:
        print_error("Failed to retrieve any hazard areas!")
        return False
    
    print_info(f"Deleting hazard area with ID: {hazard_area.hazard_id}...")
    if delete_hazard_area(hazard_area.hazard_id):
        print_success(f"Successfully deleted hazard area")
    else:
        print_error("Failed to delete hazard area!")
        return False
    
    return True

def run_all_tests():
    print_header("🚀 Starting SpaceY Database Model Tests")
    
    # Save the original get_connection function to restore later
    original_get_connection = db.get_connection
    
    try:
        # Patch the database module to use our test connection
        db.get_connection = test_get_connection
        
        # Also patch the imported module functions
        import models.rover
        import models.project  
        import models.trajectory
        import models.hazard_area
        
        # Replace the get_connection function in all modules
        models.rover.get_connection = test_get_connection
        models.project.get_connection = test_get_connection
        models.trajectory.get_connection = test_get_connection
        models.hazard_area.get_connection = test_get_connection
        
        start_time = time.time()
        
        # Set up a fresh test database
        setup_test_database()
        
        tests = [
            ("Rover", test_rover),
            ("Project", test_project),
            ("Trajectory", test_trajectory),
            ("Hazard Area", test_hazard_area)
        ]
        
        # Run the tests and collect results
        results = []
        for test_name, test_func in tests:
            print_info(f"Running {test_name} tests...")
            try:
                success = test_func()
                results.append((test_name, success))
            except Exception as e:
                print_error(f"Test threw an exception: {str(e)}")
                results.append((test_name, False))
        
        # ... (rest of function stays the same)
        
    finally:
        # Clean up: Restore the original get_connection functions
        db.get_connection = original_get_connection
        # Also restore the imported module functions if they exist
        if 'models.rover' in sys.modules:
            sys.modules['models.rover'].get_connection = original_get_connection
        if 'models.project' in sys.modules:
            sys.modules['models.project'].get_connection = original_get_connection
        if 'models.trajectory' in sys.modules:
            sys.modules['models.trajectory'].get_connection = original_get_connection
        if 'models.hazard_area' in sys.modules:
            sys.modules['models.hazard_area'].get_connection = original_get_connection
            
        teardown_test_database()
        print_info("Original database connection restored")

if __name__ == "__main__":
    run_all_tests()