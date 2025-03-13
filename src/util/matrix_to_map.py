# Author: Matthew Spagnuolo
import dem_to_matrix
import math

MARS_DEM_RESOLUTION = 200 # meters between elevation points (calculated for the .tif file used using it's source's information)

def calculate_max_delta(max_slope, diagonal=False):
    """
    Calculates the maximum elevation delta between two points that can be considered accessible
    given a maximum slope.

    :param max_slope: Maximum slope to be considered accessible (degrees)
    :param diagonal: If the slope is diagonal
    :return: Maximum elevation delta
    """
    return MARS_DEM_RESOLUTION * math.tan(math.radians(max_slope)) if not diagonal else MARS_DEM_RESOLUTION * math.tan(math.radians(max_slope)) * math.sqrt(2)

def matrix_to_map(dem_matrix, max_slope=30):
    """
    Converts a 2D matrix representing a DEM into a map by calculating elevation points and deciding if
    a cell can access a neighbor.

    This changes the original matrix by adding a new 8-tuple to each cell containing 0, 1 values to 
    indicate if the top, top-right, right, bottom-right, bottom, bottom-left, left, or top-left cells (in this order, which is clockwise) can be accessed from the current cell.

    Example:
    (1, 0, 0, 1, 1, 1, 1, 0) means that, from the current cell, one can travel to any neighboring cell, except for the top-right, right, and top-left cells.
    
    :param dem_matrix: 2D list representing the DEM with coordinates
    :param max_slope: Maximum slope to be considered accessible (degrees)
    :return: 3D list representing the DEM with each cell being a list of indexes, coordinates, elevation, and walls
    """

    max_elevation_delta = calculate_max_delta(max_slope) # Maximum elevation delta for vertical movement
    max_elevation_delta_diagonal = calculate_max_delta(max_slope, diagonal=True) # Maximum elevation delta for diagonal movement
    print(f"Max elevation delta: {max_elevation_delta}")
    print(f"Max elevation delta (diagonal): {max_elevation_delta_diagonal}")

    for row in range(len(dem_matrix)):            
        if row % 100 == 0:
                print(f"Generating walls for row {row}...")
        for col in range(len(dem_matrix[0])):

            cell = dem_matrix[row][col]
            wall_up = wall_right = wall_down = wall_left = wall_up_right = wall_down_right = wall_down_left = wall_up_left = 1
            # Handle top
            if row == 0:
                wall_up = wall_up_right = wall_up_left = 0 # Map edge
            else:
                top_cell = dem_matrix[row - 1][col]
                if abs(top_cell[2] - cell[2]) >= max_elevation_delta:
                    wall_up = 0
                # Handle top-right
                if col != len(dem_matrix[0]) - 1:
                    diag_cell = dem_matrix[row - 1][col + 1]
                    if abs(diag_cell[2] - cell[2]) >= max_elevation_delta_diagonal:
                        wall_up_right = 0
                # Handle top-left
                if col != 0:
                    diag_cell = dem_matrix[row - 1][col - 1]
                    if abs(diag_cell[2] - cell[2]) >= max_elevation_delta_diagonal:
                        wall_up_left = 0

            # Handle right
            if col == len(dem_matrix[0]) - 1:
                wall_right = wall_up_right = wall_down_right = 0 # Map edge
            else:
                right_cell = dem_matrix[row][col + 1]
                if abs(right_cell[2] - cell[2]) >= max_elevation_delta:
                    wall_right = 0

            # Handle bottom
            if row == len(dem_matrix) - 1:
                wall_down = wall_down_left = wall_down_right = 0 # Map edge
            else:
                bottom_cell = dem_matrix[row + 1][col]
                if abs(bottom_cell[2] - cell[2]) >= max_elevation_delta:
                    wall_down = 0
                # Handle bottom-right
                if col != len(dem_matrix[0]) - 1:
                    diag_cell = dem_matrix[row + 1][col + 1]
                    if abs(diag_cell[2] - cell[2]) >= max_elevation_delta_diagonal:
                        wall_down_right = 0
                # Handle bottom-left
                if col != 0:
                    diag_cell = dem_matrix[row + 1][col - 1]
                    if abs(diag_cell[2] - cell[2]) >= max_elevation_delta_diagonal:
                        wall_down_left = 0

            # Handle left
            if col == 0:
                wall_left = wall_down_left = wall_up_left = 0 # Map edge
            else:
                left_cell = dem_matrix[row][col - 1]
                if abs(left_cell[2] - cell[2]) >= max_elevation_delta:
                    wall_left = 0
            
            cell.append((wall_up, wall_up_right, wall_right, wall_down_right, wall_down, wall_down_left, wall_left, wall_up_left))

    return dem_matrix
                
if __name__ == "__main__":
    tif_file = "Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif"
    print("Reading DEM...")
    dem_matrix,_ = dem_to_matrix.dem_to_matrix(tif_file, start_point=(0, 0), max_rows=1000, max_cols=1000)
    print("Generating map...")
    print(matrix_to_map(dem_matrix, 30)) # 30 degrees maximum slope (found this from the internet)
