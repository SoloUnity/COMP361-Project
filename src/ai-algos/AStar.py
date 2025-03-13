from Pathfinder import PathFinder
from Location import Location
import heapq
import math

class AStar(PathFinder):
    """
    A* search algorithm
    """

    def goTo(self, fromLoc, toLoc, rover, mapHandler):
        """
        Finds a path from fromLoc to toLoc in the provided submap and for the provided rover
            using A* search
        Returns a list of locations corresponding to the path

        fromLoc : Location
            the starting location
        toLoc : Location
            the destination
        rover : Rover
            the rover for which the method searches a path
        mapHandler : MapHandler
            handler for the map subsection the methods searches in
        """
        
        # Priority queue for A*
        open_set = []
        # Dictionary to track g_scores (cost from start to current node)
        g_score = {}
        # Dictionary to track f_scores (g_score + heuristic)
        f_score = {}
        # Dictionary to keep track of where nodes came from
        came_from = {}
        
        # Initial setup
        start_node = (fromLoc.x, fromLoc.y)
        goal_node = (toLoc.x, toLoc.y)
        
        # Add start node to open set with priority 0
        heapq.heappush(open_set, (0, start_node))
        
        # Initialize g_score for start node
        g_score[start_node] = 0
        
        # Initialize f_score for start node (g_score + heuristic)
        f_score[start_node] = self._heuristic(start_node, goal_node)
        
        # Keep track of closed nodes
        closed_set = set()
        
        while open_set:
            # Get the node with lowest f_score
            _, current = heapq.heappop(open_set)
            
            # If we reached the goal, reconstruct and return the path
            if current == goal_node:
                path = [fromLoc]
                path_node = current
                
                while path_node in came_from:
                    x, y = path_node
                    path.append(Location(x, y, mapHandler.map[x][y][0], mapHandler.map[x][y][1], mapHandler.map[x][y][2]))
                    path_node = came_from[path_node]
                
                path = path[:-1]  # Remove the duplicate of fromLoc
                path.reverse()  # Reverse to get correct order
                return path
            
            # Add current to closed set
            closed_set.add(current)
            
            # Get current location details
            cx, cy = current
            currentLoc = Location(cx, cy, mapHandler.map[cx][cy][0], mapHandler.map[cx][cy][1], mapHandler.map[cx][cy][2])
            
            # Process all neighbors
            for neighbor in mapHandler.getNeighbors(cx, cy):
                # Skip if already evaluated
                if neighbor in closed_set:
                    continue
                
                # Create Location object for neighbor
                nx, ny = neighbor
                neighborLoc = Location(nx, ny, mapHandler.map[nx][ny][0], mapHandler.map[nx][ny][1], mapHandler.map[nx][ny][2])
                
                # Check if rover can traverse from current to neighbor
                if not rover.canTraverse(currentLoc, neighborLoc):
                    continue
                
                # Tentative g_score is current g_score + cost to neighbor
                # Here we're using 1 as the basic cost, but could be modified for terrain difficulty
                tentative_g_score = g_score[current] + 1
                
                # If we haven't seen this neighbor yet, or if this path is better
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Record this path
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self._heuristic(neighbor, goal_node)
                    
                    # Add to open set if not already there
                    if not any(neighbor == node for _, node in open_set):
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # If we get here, no path was found
        return []

    def visitAll(self, fromLoc, toVisit, rover, mapHandler):
        """
        Finds a path from fromLoc that visits the locations in toVisit in the provided submap and for the provided rover
            using A* search
        Returns a list of locations corresponding to the path

        fromLoc : Location
            the starting location
        toVisit : List[Location]
            the destination
        rover : Rover
            the rover for which the method searches a path
        mapHandler : MapHandler
            handler for the map subsection the methods searches in
        """
        
        path = [fromLoc]
        if (len(toVisit) == 0): return path

        leftToVisit = set(map(lambda loc: (loc.x, loc.y), toVisit))
        currentLoc = fromLoc
        
        while leftToVisit:
            # Find the closest location to visit next
            closest_loc = None
            closest_path = None
            min_distance = float('inf')
            
            for loc_coord in leftToVisit:
                to_loc = self._coord_to_location(loc_coord, mapHandler)
                temp_path = self.goTo(currentLoc, to_loc, rover, mapHandler)
                
                # If a path exists and it's shorter than the current minimum
                if temp_path and (len(temp_path) - 1) < min_distance:  # -1 because goTo includes currentLoc
                    min_distance = len(temp_path) - 1
                    closest_loc = loc_coord
                    closest_path = temp_path
            
            # If we found a path to at least one location
            if closest_loc:
                # Skip the first location which is the current location
                path.extend(closest_path[1:])
                leftToVisit.remove(closest_loc)
                currentLoc = self._coord_to_location(closest_loc, mapHandler)
            else:
                # If no path was found to any remaining location, break
                break
        
        return path

    def _heuristic(self, a, b):
        """
        Calculate Manhattan distance heuristic between two points
        
        a : tuple (x, y)
        b : tuple (x, y)
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def _coord_to_location(self, coord, mapHandler):
        """
        Convert coordinates to Location object
        
        coord : tuple (x, y)
        mapHandler : MapHandler
        """
        x, y = coord
        return Location(x, y, mapHandler.map[x][y][0], mapHandler.map[x][y][1], mapHandler.map[x][y][2])