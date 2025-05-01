from core.node import Node


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
