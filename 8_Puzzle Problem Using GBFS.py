import heapq

class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.cost = cost  # For GBFS, we don't use this, but it can be useful for comparison
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.heuristic < other.heuristic
def greedy_best_first_search(start, goal, get_neighbors, heuristic):
    # Priority queue to store the frontier nodes, ordered by the heuristic
    frontier = []
    heapq.heappush(frontier, Node(start, heuristic=heuristic(start, goal)))
    
    # Set to track visited nodes
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
