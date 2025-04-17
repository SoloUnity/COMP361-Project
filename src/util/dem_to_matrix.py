# Author: Matthew Spagnuolo
import rasterio
from rasterio.windows import Window

def dem_to_matrix(tif_path, start_point=(0, 0), max_rows=1000, max_cols=1000):
    """
    Reads a .tif DEM file and converts it into a 2D matrix where each cell contains:
    [index, (latitude, longitude), elevation].

    :param tif_path: Path to the .tif DEM file
    :param start_point: Tuple with the row and column to start reading the DEM
    :param max_rows: Maximum number of rows to read, has to be less than 10,000
    :param max_cols: Maximum number of columns to read, has to be less than 50,000
    :return: 2D list representing the DEM with coordinates
    """

    if max_rows > 10000 or max_cols > 50000:
        raise ValueError("The maximum number of rows is 10,000 and the maximum number of columns is 50,000.")
    
    new_transform = None
    with rasterio.open(tif_path) as dataset:
        full_transform = dataset.transform
        window = Window(start_point[1], start_point[0], max_cols, max_rows)
        
        new_transform = rasterio.windows.transform(window, full_transform)

        # Read only the area we need
        dem_matrix = dataset.read(1, window=window)
        # Get the transform for this window so that pixel coordinates map correctly.
        transform = dataset.window_transform(window)
        
        indexed_matrix = []
        for row in range(dem_matrix.shape[0]):
            if row % 100 == 0:
                print(f"Processing cells for row {row}...")
            row_list = []
            for col in range(dem_matrix.shape[1]):
                # Compute global indices if needed
                global_row = row + start_point[0]
                global_col = col + start_point[1]
                # Convert the local (col, row) to geographic coordinates.
                lon, lat = transform * (col, row)
                elevation = float(dem_matrix[row, col])
                row_list.append([(global_row, global_col), (lat, lon), elevation])
            indexed_matrix.append(row_list)

    return indexed_matrix, new_transform

def get_window_for_path(tif_path, latlon_path, buffer=10):
    """
    Given a list of (lat, lon) tuples, compute the (row, col) start_point
    and the number of rows and columns needed to cover all points,
    plus an optional buffer in pixels.

    :param tif_path: Path to the .tif DEM file
    :param latlon_path: List of (lat, lon) tuples defining the path
    :param buffer: Number of extra pixels to include around the bounding box
    :return: ((start_row, start_col), num_rows, num_cols)
    """
    with rasterio.open(tif_path) as ds:
        # Convert each lat/lon to (row, col) in the raster
        idx = [ds.index(lon, lat) for lat, lon in latlon_path]
        rows, cols = zip(*idx)

        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        # Apply buffer, clamped to image bounds
        start_row = max(min_row - buffer, 0)
        start_col = max(min_col - buffer, 0)
        num_rows = (max_row - min_row + 1) + 2 * buffer
        num_cols = (max_col - min_col + 1) + 2 * buffer

        # Compute relative indices for each waypoint within the window
        rel_indices = []
        for lat, lon in latlon_path:
            full_row, full_col = ds.index(lon, lat)
            rel_row = full_row - start_row
            rel_col = full_col - start_col
            rel_indices.append((rel_row, rel_col))

    return (start_row, start_col), num_rows, num_cols, rel_indices

if __name__ == "__main__":
    tif_file = "Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif"  
    dem_to_matrix(tif_file)