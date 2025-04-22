class Node:
    def __init__(self, data, x, y, row, col):
        self.x = x
        self.y = y
        self.data = data
        self.row = row
        self.col = col
        self.friend = []
        self.parent = None
        self.g_cost = float('inf')
        self.h_cost = float('inf')
        self.pheromone = 1.0

    def f_cost(self):
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        return self.f_cost() < other.f_cost()