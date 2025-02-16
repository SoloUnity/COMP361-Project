from config.db_config import get_connection

def fetch_rovers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Rover")
    rovers = cursor.fetchall()
    conn.close()
    return rovers

def fetch_trajectory(rover_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Trajectory WHERE RoverID = %s", (rover_id,))
    trajectory = cursor.fetchall()
    conn.close()
    return trajectory