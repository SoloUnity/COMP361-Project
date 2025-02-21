import math


def compute_path_distance(path, vertical=200, horizontal=110):
    total_distance = 0.0
    for i in range(1, len(path)):
        r1, c1 = path[i-1]
        r2, c2 = path[i]
        dr = abs(r2 - r1)
        dc = abs(c2 - c1)
        
        # Determine if move is vertical, horizontal, or diagonal.
        if dr == 1 and dc == 0:
            step = vertical
        elif dr == 0 and dc == 1:
            step = horizontal
        elif dr == 1 and dc == 1:
            step = math.sqrt(vertical**2 + horizontal**2)
        else:
            # For moves that span more than one cell, adjust accordingly:
            step = math.sqrt((vertical * dr)**2 + (horizontal * dc)**2)
        
        total_distance += step
    return total_distance