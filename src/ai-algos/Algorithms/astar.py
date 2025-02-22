import heapq
import math

from ..util.compute_path_distance import compute_path_distance
from ..util.latlon_to_index import latlon_to_index
from ..util.matrix_to_map import matrix_to_map
from ..util.dem_to_matrix import dem_to_matrix

MARS_DEM_RESOLUTION = 200

def astar_path(map_data, start, goal):
    """
    Finds the shortest path on the preprocessed map_data from start to goal.
    
    :param map_data: 2D list output by matrix_to_map where each cell is
                     [ (row, col), (lat, lon), elevation, (flag_top, flag_top_right, ..., flag_top_left) ]
    :param start: Tuple (row, col) for the start cell.
    :param goal: Tuple (row, col) for the goal cell.
    :return: List of (row, col) tuples representing the path from start to goal, or None if no path exists.
    """
    # Define the 8 possible movement directions in the same order as the flags.
    directions = [
        (-1,  0),  # top
        (-1,  1),  # top-right
        ( 0,  1),  # right
        ( 1,  1),  # bottom-right
        ( 1,  0),  # bottom
        ( 1, -1),  # bottom-left
        ( 0, -1),  # left
        (-1, -1)   # top-left
    ]
    
    # Movement costs: straight moves cost the DEM resolution, diagonal moves cost resolution*sqrt(2)
    cost_straight = MARS_DEM_RESOLUTION
    cost_diagonal = MARS_DEM_RESOLUTION * math.sqrt(2)
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    
    while open_set:
        current_priority, current = heapq.heappop(open_set)
        
        if current == goal:
            break
        
        current_row, current_col = current
        # Each cell is structured as [ (row, col), (lat, lon), elevation, accessibility_flags ]
        current_cell = map_data[current_row][current_col]
        accessible_flags = current_cell[3]
        
        # Check all 8 neighbors
        for i, (dr, dc) in enumerate(directions):
            # Only consider this neighbor if the flag indicates accessibility.
            if accessible_flags[i] == 0:
                continue

            neighbor = (current_row + dr, current_col + dc)
            
            # Check bounds.
            if (neighbor[0] < 0 or neighbor[0] >= len(map_data) or 
                neighbor[1] < 0 or neighbor[1] >= len(map_data[0])):
                continue
            
            # Choose the movement cost based on direction (diagonal or straight).
            move_cost = cost_straight if i % 2 == 0 else cost_diagonal
            new_cost = cost_so_far[current] + move_cost
            
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                
                # Use an octile distance as the heuristic.
                dx = abs(goal[0] - neighbor[0])
                dy = abs(goal[1] - neighbor[1])
                heuristic = min(dx, dy) * cost_diagonal + abs(dx - dy) * cost_straight
                priority = new_cost + heuristic
                
                heapq.heappush(open_set, (priority, neighbor))
                came_from[neighbor] = current
                    
    # If the goal was never reached, return None.
    if goal not in came_from:
        return None
    
    # Reconstruct the path from goal to start.
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

if __name__ == "__main__":
    dem_matrix, new_transform = dem_to_matrix("Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif", start_point=(10000, 28000), max_rows=1000, max_cols=1000)
    map_data = matrix_to_map(dem_matrix, max_slope=30)
    
    start_lat, start_lon = 53.34412, -84.78836
    goal_lat, goal_lon = 53.37433, -84.49997

    start_row, start_col  = latlon_to_index(start_lat, start_lon, new_transform)
    goal_row, goal_col  = latlon_to_index(goal_lat, goal_lon, new_transform)

    print("Start index:", start_row, start_col)
    print("Goal index:", goal_row, goal_col)
    
    path = astar_path(map_data, (start_row, start_col), (goal_row, goal_col))
    if path is not None:
        print("Path found:")
        for r, c in path:
            print(f"({r}, {c})")
        
        distance = compute_path_distance(path)
        print(f"Total distance: {distance:.0f} meters")
    else:
        print("No path found.")
