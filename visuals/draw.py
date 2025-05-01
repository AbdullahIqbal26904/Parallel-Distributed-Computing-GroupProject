import time
import turtle
import _tkinter


class Draw(turtle.Turtle):
    def __init__(self, is_player):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.shapesize(2, 2)
        self.penup()
        self.speed(0)
        self.hideturtle()
        if is_player == "p":
            self.color("orange")
        elif is_player == "W":
            self.color("red")
        elif is_player == "B":
            self.color("orange")
        elif is_player == "F":
            self.shape("square")
            self.shapesize(1)
            self.color("blue")
            self.hideturtle()
        elif is_player == "pheromone":
            self.shape("square")
            self.shapesize(1)
            self.color("green")
            self.hideturtle()
        else:
            self.shape("circle")
            self.color("gold")
            self.hideturtle()
            self.gold = 100

    def change_color(self):
        self.color("green")


# Function to display the maze with the best path
def display_maze_with_path(maze, path):
    maze_copy = [list(row) for row in maze]
    for node in path:
        if maze_copy[node.row][node.col] not in ('p', 'G'):
            maze_copy[node.row][node.col] = 'F'
    print("\nMaze with the final path:")
    for row in maze_copy:
        print(''.join(row))


def setup_maze(maze, pen, player, goal):
    grid_drawer = turtle.Turtle()
    grid_drawer.color("white")
    grid_drawer.speed(0)
    grid_drawer.penup()
    num_cells_y = 15
    num_cells_x = 25
    cell_size = 50
    start_x = -625  # Starting x coordinate
    start_y = 375
    for i in range(num_cells_x + 1):
        x = start_x + i * cell_size
        grid_drawer.goto(x, start_y)
        grid_drawer.pendown()
        grid_drawer.goto(x, start_y - num_cells_y * cell_size)
        grid_drawer.penup()
    for i in range(num_cells_y + 1):
        y = start_y - i * cell_size
        grid_drawer.goto(start_x, y)
        grid_drawer.pendown()
        grid_drawer.goto(start_x + num_cells_x * cell_size, y)
        grid_drawer.penup()

    grid_drawer.hideturtle()
    try:
        cell_info = turtle.Turtle()
        cell_info.hideturtle()
        cell_info.penup()
        pen.speed(100000)
        cell_info.speed(1000000)
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                character = maze[y][x]
                screen_x = -600 + (x * 50)
                screen_y = 350 - (y * 50)
                if character == "G":
                    goal.goto(screen_x, screen_y)
                    goal.stamp()
                    cell_info.goto(screen_x, screen_y)
                    cell_info.color("black")
                    cell_info.write(f"Goal", align="center", font=("Arial", 12, "normal"))
                if character == "p":
                    player.goto(screen_x, screen_y)
                    player.stamp()
                    cell_info.goto(screen_x, screen_y)
                    cell_info.color("black")
                    cell_info.write(f"Start", align="center", font=("Arial", 12, "normal"))
                if character == "X":
                    pen.goto(screen_x, screen_y)
                    pen.stamp()
                    cell_info.goto(screen_x, screen_y)
                    cell_info.color("black")
                    cell_info.write(f"Wall", align="center", font=("Arial", 12, "normal"))
    except _tkinter.TclError as e:
        pass


def create_thread_turtles(colors):
    """Create multiple turtles for parallel path visualization."""
    turtles = []
    for color in colors:
        t = Draw("B")
        t.color(color)
        t.hideturtle()
        turtles.append(t)
    return turtles


def update_visualization(screen, queue, path_queue, thread_colors):
    """Process-safe visualization updater."""
    turtles = [turtle.Turtle() for _ in thread_colors]
    for t, color in zip(turtles, thread_colors):
        t.shape("square")
        t.shapesize(1.5)
        t.color(color)
        t.penup()
        t.speed(0)
        t.hideturtle()

    final_path_turtle = turtle.Turtle()
    final_path_turtle.color("blue")
    final_path_turtle.penup()
    final_path_turtle.hideturtle()

    while True:
        while not queue.empty():
            node, color_id = queue.get()
            turtles[color_id].goto(node.x, node.y)
            turtles[color_id].stamp()

        if not path_queue.empty():
            path = path_queue.get()
            for node in reversed(path):
                final_path_turtle.goto(node.x, node.y)
                final_path_turtle.stamp()
            break

        screen.update()
        # time.sleep(0.01)
def create_dijkstra_turtles(colors):
    """Create colored turtles for parallel Dijkstra visualization."""
    turtles = []
    for color in colors:
        t = Draw("B")
        t.color(color)
        t.shapesize(1.5)  # Slightly smaller for clarity
        turtles.append(t)
    return turtles


def reset_maze(path, finalPath):
    path.clear()
    finalPath.clear()
