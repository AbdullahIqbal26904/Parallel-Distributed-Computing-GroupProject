from core.priority_queue import PriorityQueue
import math
import time


def findIndex(list, node):
    for ff in range(len(list)):
        if node.data == list[ff].data and node.x == list[ff].x and node.y == list[ff].y and node.row == list[
            ff].row and node.col == list[ff].col:
            return ff


def heuristic(x, y, goal):
    a = math.pow((goal.x - x), 2)
    b = math.pow((goal.y - y), 2)
    sum = a + b
    sum = math.sqrt(sum)
    return sum


def A_star_Search(start, goal, mazeList, path, finalPath, goal_pen):
    queue = PriorityQueue()
    visited = []
    parent = []
    index2 = 0
    queue.put(start, 0)
    for i in range(len(mazeList)):
        visited.append(0)
    for i in range(len(mazeList)):
        parent.append(None)
    visited[0] = 1
    while queue.peek() != goal:
        vertex = queue.get()
        if vertex.data != "p":
            path.goto(vertex.x, vertex.y)
            path.speed(0)
            time.sleep(0.1)
            path.stamp()
        for neighbours in vertex.friend:
            neighbours.g_cost = vertex.g_cost + 20
            neighbours.h_cost = heuristic(neighbours.x, neighbours.y, goal)
            f_cost = neighbours.f_cost()
            index = findIndex(mazeList, neighbours)
            if visited[index] != 1 and neighbours.data != "X":
                visited[index] = 1
                queue.put(neighbours, f_cost)
                parent[index] = vertex
                if neighbours.data == "G":
                    print(True)
                    print(index)
                    index2 = index
                    goal_pen.color("red")
    while parent[index2].data != start.data:
        node = parent[index2]
        index2 = findIndex(mazeList, node)
        finalPath.goto(node.x, node.y)
        finalPath.stamp()
        finalPath.speed(0)
