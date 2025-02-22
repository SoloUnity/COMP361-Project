class MapHandler:
    def __init__(self, mapData):
        self.map = mapData
        self.width = len(mapData)
        self.height = len(mapData[0])
    
    def getAltitude(self, x, y):
        return self.map[x][y][2]
    
    def isValidLocation(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def getNeighbors(self, x, y):
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newX, newY = x + dx, y + dy
            if self.isValidLocation(newX, newY):
                neighbors.append((newX, newY))
        return neighbors
    
    def getMapSection(self, startX, startY, width, height):
        endX = min(startX + width, self.width)
        endY = min(startY + height, self.height)
        return [row[startY:endY] for row in self.map[startX:endX]]