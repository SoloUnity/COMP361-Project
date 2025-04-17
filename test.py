from src.ai_algos.Rover import Rover
from src.util.dem_to_matrix import dem_to_matrix
from src.ai_algos.MapHandler import MapHandler
from src.ai_algos.DFS import DFS

mapFilePath = "./Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.tif"

matrix, new_transform = dem_to_matrix(mapFilePath, (5000, 4030), 200, 200)
mH = MapHandler(matrix)
fromLoc = mH.getLocationAt(10, 10)
toLoc1 = mH.getLocationAt(150, 150)
rover = Rover(5)
dfs = DFS()
path = dfs.visitAll(fromLoc, [toLoc1], rover, mH)
for loc in path:
    loc.printLoc()