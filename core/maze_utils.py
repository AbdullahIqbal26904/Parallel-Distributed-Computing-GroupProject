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


def createFriendsList(listOfNodes):
    root = None
    goal = None
    node_dict = {(node.x, node.y): node for node in listOfNodes}
    for node in listOfNodes:
        if node.data == "p":
            root = node
            node.g_cost = 0
        else:
            node.g_cost = 20
        if node.data == "G":
            goal = node
        positions = [(50, 0), (-50, 0), (0, 50), (0, -50)]
        for dx, dy in positions:
            neighbor_x = node.x + dx
            neighbor_y = node.y + dy
            if (neighbor_x, neighbor_y) in node_dict:
                neighbor = node_dict[(neighbor_x, neighbor_y)]
                node.friend.append(neighbor)
                neighbor.parent = node
    return root, goal
