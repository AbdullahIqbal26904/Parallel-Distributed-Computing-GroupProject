# Parallel & Distributed Computing - Maze Solver

A visual maze solver application that implements various pathfinding algorithms in both sequential and parallel forms.

## Project Overview

This project demonstrates the application of parallel computing techniques to traditional pathfinding algorithms. The application visualizes the maze solving process and shows performance improvements achieved through parallelization.

## Features

- Visual representation of maze solving algorithms
- Implementation of multiple pathfinding algorithms:
  - A* Search
  - Dijkstra's Algorithm
  - Bellman-Ford Algorithm
  - Parallel Delta-Stepping Dijkstra
  - Parallel A* Search
- Performance metrics for comparing sequential vs. parallel implementations
- Interactive visualization using Python's Turtle graphics

## Installation

### Prerequisites

- Python 3.6+
- Multiprocessing support

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Parallel-Distributed-Computing.git
cd Parallel-Distributed-Computing
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script to start the application:

```bash
python main.py
```

When prompted, select an algorithm:
1. A* Search
2. Dijkstra's Algorithm
3. Bellman-Ford Algorithm
4. Parallel Dijkstra (Delta-Stepping)
5. Parallel A* Search

For parallel algorithms, you can specify:
- Number of processes (or 0 for auto-detection)
- Delta value (for Delta-Stepping algorithm)

## Algorithms

### A* Search
A* is an informed search algorithm that optimizes path finding by using a heuristic function to guide the search. It guarantees the shortest path when using an admissible heuristic.

### Dijkstra's Algorithm
Dijkstra's algorithm finds the shortest path from a start node to all other nodes in a weighted graph. It uses a priority queue to efficiently process nodes in order of increasing distance.

### Bellman-Ford Algorithm
Bellman-Ford finds the shortest path from a start node to all other nodes, even in graphs with negative edge weights. It iteratively relaxes all edges.

### Parallel Delta-Stepping Dijkstra
A parallel implementation of Dijkstra's algorithm that divides nodes into buckets based on distance, allowing concurrent processing of nodes within the same distance range.

### Parallel A* Search
A parallel implementation of A* that distributes the processing of neighbor nodes across multiple processes, improving exploration speed while maintaining optimality.

## Project Structure

```
.
├── algorithms/               # Algorithm implementations
│   ├── a_star.py            # Sequential A* implementation
│   ├── dijkstra.py          # Sequential Dijkstra implementation
│   ├── bellman_ford.py      # Sequential Bellman-Ford implementation  
│   ├── parallel_dijkstra.py # Parallel Delta-Stepping Dijkstra
│   └── parallel_astar.py    # Parallel A* implementation
├── core/                     # Core data structures
│   ├── node.py              # Node representation
│   ├── priority_queue.py    # Priority queue implementation
│   └── maze_utils.py        # Maze utility functions
├── visuals/                  # Visualization components
│   └── draw.py              # Drawing utilities
├── main.py                   # Main application entry point
├── maze.txt                  # Sample maze definition
└── requirements.txt          # Project dependencies
```

## Performance Comparison

The parallel implementations generally outperform their sequential counterparts, especially on larger mazes and multi-core systems. The actual performance improvement depends on:

- Maze size and complexity
- Available CPU cores
- Algorithm parameters (like delta value for Delta-Stepping)

## Creating Custom Mazes

Mazes are defined in text files with the following notation:
- `X`: Wall
- `p`: Start position
- `G`: Goal position
- `b`: Open space

To create a custom maze, edit the `maze.txt` file or create a new one with the same format.