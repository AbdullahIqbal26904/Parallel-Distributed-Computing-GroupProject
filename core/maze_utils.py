from core.node import Node
import random

def generate_maze(width, height, wall_density=0.2):
    """Generate a random maze of specified dimensions.
    
    Args:
        width: Width of the maze
        height: Height of the maze
        wall_density: Probability of a cell being a wall (0.0 to 1.0)
        
    Returns:
        2D list representing the maze
    """
    maze = []
    
    # Generate random maze with specified wall density
    for y in range(height):
        row = []
        for x in range(width):
            # First column and last row/column are walls
            if x == 0 or y == height-1 or x == width-1:
                row.append('X')
            # Place start position in top-left corner
            elif x == 1 and y == 1:
                row.append('p')
            # Place goal in bottom-right corner (not on edge)
            elif x == width-2 and y == height-2:
                row.append('G')
            # Random walls or open spaces elsewhere
            else:
                if random.random() < wall_density:
                    row.append('X')
                else:
                    row.append('b')
        maze.append(row)
    
    # Ensure a path exists from start to goal using a simple flood fill check
    # (This is a basic implementation - might need to be refined)
    ensure_path_exists(maze, 1, 0, width-2, height-2)
    
    return maze

def ensure_path_exists(maze, start_x, start_y, goal_x, goal_y):
    """Ensure there is a valid path from start to goal."""
    # Simple solution: create a corridor from start to goal
    # This could be improved with more sophisticated maze generation
    
    # Horizontal corridor to almost goal_x
    x = start_x
    while x < goal_x:
        maze[start_y][x] = 'b'
        x += 1
    
    # Vertical corridor to goal_y
    y = start_y
    while y < goal_y:
        maze[y][x] = 'b'
        y += 1
    
    # Ensure goal is accessible
    maze[goal_y][goal_x] = 'G'

def read_File_Create_List(filename):
    with open(filename, 'r') as file:
        content = file.readlines()
    data_2d = []
    for line in content:
        row = list(line.strip())
        data_2d.append(row)
    return data_2d


def createNodes(maze):
    listOfNodes = []
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            character = maze[y][x]
            screen_x = -600 + (x * 50)
            screen_y = 350 - (y * 50)
            node = Node(character, screen_x, screen_y, y, x)
            listOfNodes.append(node)
    return listOfNodes


def createFriendsList(nodes):
    root, goal = None, None
    edges = []
    node_dict = {(node.x, node.y): node for node in nodes}
    for node in nodes:
        if node.data == "p":
            root = node
            node.g_cost = 0
        if node.data == "G":
            goal = node
        for dx, dy in [(50, 0), (-50, 0), (0, 50), (0, -50)]:
            neighbor = node_dict.get((node.x + dx, node.y + dy))
            # Skip walls and invalid neighbors
            if neighbor and neighbor.data != "X":  # <--- KEY CHANGE HERE
                node.friend.append(neighbor)
                edges.append((node, neighbor, 20))  # Edge weight = 20
    return root, goal, edges
