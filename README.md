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
- Performance comparison and visualization tools

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

## Performance Testing

To run performance tests comparing sequential and parallel implementations:

```bash
# For Dijkstra performance comparison
python performance_comparision.py

# For A* performance comparison
python peformance_comparision_astar.py
```

The performance tests will generate visualizations comparing execution times and speedups.

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
├── algorithms/                   # Algorithm implementations
│   ├── a_star.py                # Sequential A* implementation
│   ├── dijkstra.py              # Sequential Dijkstra implementation
│   ├── BellmanFord_v5.py        # Sequential & Parallel Bellman-Ford  
│   ├── parallel_dijkstra.py     # Parallel Delta-Stepping Dijkstra
│   └── parallel_astar.py        # Parallel A* implementation
├── core/                         # Core data structures
│   ├── node.py                  # Node representation
│   ├── priority_queue.py        # Priority queue implementation
│   └── maze_utils.py            # Maze utility functions & generation
├── visuals/                      # Visualization components
│   └── draw.py                  # Drawing utilities for maze visualization
├── main.py                       # Main application entry point
├── performance_comparision.py    # Performance testing for Dijkstra
├── peformance_comparision_astar.py # Performance testing for A*
├── bellman_ford_results.csv      # Performance results for Bellman-Ford
├── maze.txt                      # Sample maze definition
└── requirements.txt              # Project dependencies
```

## Performance Comparison

The parallel implementations generally outperform their sequential counterparts, especially on larger mazes and multi-core systems. The actual performance improvement depends on:

- Maze size and complexity
- Available CPU cores
- Algorithm parameters (like delta value for Delta-Stepping)

The repository includes performance comparison visualizations:
- `dijkstra_performance_comparison.png` - Performance comparison for Dijkstra algorithms
- `astar_performance_comparison.png` - Performance comparison for A* algorithms
- `execution_time.png` - Bellman-Ford execution time comparison
- `speedup.png` - Bellman-Ford speedup visualization

## Creating Custom Mazes

Mazes are defined in text files with the following notation:
- `X`: Wall
- `p`: Start position
- `G`: Goal position
- `b`: Open space

To create a custom maze, edit the `maze.txt` file or create a new one with the same format. You can also use the `generate_maze()` function in `core/maze_utils.py` to programmatically generate random mazes of any size.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.