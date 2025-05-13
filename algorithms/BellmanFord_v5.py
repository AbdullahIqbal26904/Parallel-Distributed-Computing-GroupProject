import numpy as np
import time
import multiprocessing as mp
import matplotlib.pyplot as plt
import pandas as pd

# Generate a random directed graph
def generate_graph(nodes, density=0.1):
    edges = []
    num_edges = int(nodes * nodes * density)
    for _ in range(num_edges):
        u = np.random.randint(0, nodes)
        v = np.random.randint(0, nodes)
        if u != v:
            weight = np.random.randint(1, 99)
            edges.append((u, v, weight))
    return edges, nodes

# Serial Bellman-Ford
def bellman_ford_serial(graph, nodes, source=0):
    distances = [float('inf')] * nodes
    distances[source] = 0

    for _ in range(nodes - 1):
        updated = False
        for u, v, w in graph:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                updated = True
        if not updated:
            break  # No updates made, so we can exit early

    # Final check for negative weight cycle
    for u, v, w in graph:
        if distances[u] != float('inf') and distances[u] + w < distances[v]:
            raise ValueError("Graph contains negative weight cycle")


# Worker: returns list of (v, new_distance) proposals
def relax_edges_worker(args):
    chunk, distances_snapshot = args
    proposals = []
    for u, v, w in chunk:
        if distances_snapshot[u] != float('inf') and distances_snapshot[u] + w < distances_snapshot[v]:
            proposals.append((v, distances_snapshot[u] + w))
    return proposals

# Parallel Bellman-Ford with synchronized updates
def bellman_ford_parallel(graph, nodes, source=0, num_processes=None):
    if num_processes is None:
        num_processes = mp.cpu_count()

    manager = mp.Manager()
    distances = manager.list([float('inf')] * nodes)
    distances[source] = 0

    pool = mp.Pool(processes=num_processes)

    edges_per_process = max(1, len(graph) // num_processes)
    edge_chunks = [graph[i:i + edges_per_process] for i in range(0, len(graph), edges_per_process)]

    for _ in range(nodes - 1):
        snapshot = list(distances)
        args = [(chunk, snapshot) for chunk in edge_chunks]
        results = pool.map(relax_edges_worker, args)

        updated = False
        for proposals in results:
            for v, new_dist in proposals:
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    updated = True

        if not updated:
            break

    pool.close()
    pool.join()

    # Final check for negative cycles
    snapshot = list(distances)
    for u, v, w in graph:
        if snapshot[u] != float('inf') and snapshot[u] + w < snapshot[v]:
            raise ValueError("Graph contains negative weight cycle")

    return list(distances)

# Performance comparison
def compare_performance(node_range, density=0.1):
    num_processes = mp.cpu_count()
    results = []

    for nodes in node_range:
        graph, _ = generate_graph(nodes, density)

        try:
            start_time = time.time()
            bellman_ford_serial(graph, nodes)
            serial_time = time.time() - start_time
        except ValueError as e:
            print(f"[Serial] Graph with {nodes} nodes contains negative cycle: Skipping")
            continue

        try:
            start_time = time.time()
            bellman_ford_parallel(graph, nodes, num_processes=num_processes)
            parallel_time = time.time() - start_time
        except ValueError as e:
            print(f"[Parallel] Graph with {nodes} nodes contains negative cycle: Skipping")
            continue

        speedup = serial_time / parallel_time if parallel_time > 0 else 1.0

        results.append({
            'Nodes': nodes,
            'Serial Time (s)': serial_time,
            'Parallel Time (s)': parallel_time,
            'Speedup': speedup
        })
        print(f"Nodes: {nodes}, Serial: {serial_time:.4f}s, Parallel: {parallel_time:.4f}s, Speedup: {speedup:.2f}x")

    return results, num_processes

# Visualization
def visualize_results(results, num_processes):
    df = pd.DataFrame(results)

    plt.figure(figsize=(10, 5))
    plt.plot(df['Nodes'], df['Serial Time (s)'], label='Serial Time', marker='o')
    plt.plot(df['Nodes'], df['Parallel Time (s)'], label=f'Parallel Time ({num_processes} processes)', marker='s')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs. Number of Nodes')
    plt.legend()
    plt.grid(True)
    plt.savefig('execution_time.png')
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(df['Nodes'], df['Speedup'], label='Speedup', marker='^', color='green')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Speedup (Serial/Parallel)')
    plt.title('Speedup vs. Number of Nodes')
    plt.legend()
    plt.grid(True)
    plt.savefig('speedup.png')
    plt.close()

# Save results to CSV
def save_results_to_csv(results, num_processes):
    df = pd.DataFrame(results)
    df['Processes'] = num_processes
    df.to_csv('bellman_ford_results.csv', index=False)
    print("Results saved to bellman_ford_results.csv")

# Main execution
if __name__ == '__main__':
    node_range = [400, 900, 1600, 3600, 6400]

    print(f"Running performance comparison with {mp.cpu_count()} available processes...")
    results, num_processes = compare_performance(node_range)

    if results:
        print("\nGenerating visualizations...")
        visualize_results(results, num_processes)

        print("\nSaving results to CSV...")
        save_results_to_csv(results, num_processes)

    print("\nDone! Check 'execution_time.png', 'speedup.png', and 'bellman_ford_results.csv'.")
