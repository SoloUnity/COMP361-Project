# Author: Matthew Spagnuolo
import rasterio

def read_tif_to_matrix(tif_path, start_point=(0, 0), max_rows=1000, max_cols=1000):
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
    
    with rasterio.open(tif_path) as dataset:
        dem_matrix = dataset.read(1)  
        transform = dataset.transform  
        rows, cols = dem_matrix.shape
        indexed_matrix = []

        for row in range(start_point[0], max_rows):
            if row % 100 == 0:
                print(f"Processing cells for row {row}...")
            row_list = []
            for col in range(start_point[1], max_cols):
                lon, lat = transform * (col, row)  
                elevation = float(dem_matrix[row, col])
                row_list.append([(row, col), (lat, lon), elevation])
            indexed_matrix.append(row_list)

    return indexed_matrix

if __name__ == "__main__":
    tif_file = "Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif"  
    read_tif_to_matrix(tif_file)