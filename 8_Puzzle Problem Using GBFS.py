import heapq

class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.cost = cost  # For GBFS, we don't use this, but it can be useful for comparison
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.heuristic < other.heuristic

