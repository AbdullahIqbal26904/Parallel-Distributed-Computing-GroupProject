from visuals.draw import Draw
from visuals.draw import reset_maze
from visuals.draw import setup_maze
import turtle
from core.maze_utils import read_File_Create_List
from core.maze_utils import createNodes
from core.maze_utils import createFriendsList
from  algorithms.a_star import A_star_Search
from  algorithms.dijkstra import dijkstra_search
if __name__ == '__main__':
    user_input = int(input(
        "Enter 1 for A*, 2 for Dijkstra: "))
    filename = "maze.txt"
    print(filename)
    Wall = Draw("W")
    Start = Draw("p")
    goal_pen = Draw("G")
    path = Draw("B")
    finalPath = Draw("F")
    pen_for_pheromone = Draw("pheromone")
    wn = turtle.Screen()
    wn.bgcolor("black")
    wn.title("Maze Solver")
    wn.setup(1400, 800)
    maze_list = read_File_Create_List(filename)
    n = createNodes(maze_list)
    root, goal_node = createFriendsList(n)
    wn.onkey(lambda: reset_maze(path, finalPath), 'r')

    if user_input == 1:
        setup_maze(maze_list, Wall, Start, goal_pen)
        A_star_Search(root, goal_node, n, path, finalPath, goal_pen)
    elif user_input == 2:
        setup_maze(maze_list, Wall, Start, goal_pen)
        dijkstra_search(root, goal_node, n, maze_list, path, finalPath, goal_pen)  # Pass maze_

    wn.mainloop()