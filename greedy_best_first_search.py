import heapq

class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.cost = cost  
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.heuristic < other.heuristic

def greedy_best_first_search(start, goal, get_neighbors, heuristic):

    frontier = []
    heapq.heappush(frontier, Node(start, heuristic=heuristic(start, goal)))
    
    visited = set()

    while frontier:
        # Get the node with the lowest heuristic value
        current_node = heapq.heappop(frontier)
        current_state = current_node.state

        # If the goal is reached, return the path
        if current_state == goal:
            return reconstruct_path(current_node)

        visited.add(current_state)

        # Explore neighbors
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                heuristic_value = heuristic(neighbor, goal)
                heapq.heappush(frontier, Node(neighbor, current_node, heuristic=heuristic_value))

    return None  # If no path is found

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

# Example heuristic function (Manhattan distance for grid-based problems)
def manhattan_heuristic(node, goal):
    x1, y1 = node
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)

# Example usage
def get_neighbors(node):
    # Placeholder: Modify based on your problem
    x, y = node
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

start = (0, 0)
goal = (4, 4)

path = greedy_best_first_search(start, goal, get_neighbors, manhattan_heuristic)
print("Path found:", path)
