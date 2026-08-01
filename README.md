# Global Dependency Risk Simulator

## Overview

The Global Dependency Risk Simulator is a Python application that models relationships among global resources, industries, infrastructure systems, and services using a directed graph.

The application demonstrates how a disruption affecting one entity can propagate to connected entities. Impact values are calculated using dependency strength and destination criticality.

Phase 3 extends the original proof of concept with caching, faster duplicate-edge detection, synthetic dataset generation, stress testing, runtime measurement, memory analysis, and performance visualization.

## Features

- Directed adjacency-list graph
- Entity and dependency insertion
- Entity and dependency deletion
- Average O(1) entity lookup
- Average O(1) duplicate dependency checks
- Breadth-First Search traversal
- Cascading risk simulation
- Impact ranking and readable summaries
- Cached repeated simulations
- Automatic cache invalidation after graph changes
- Synthetic large-scale graph generation
- Runtime and memory benchmarking
- CSV result export
- Performance graph generation
- Automated tests using pytest

## Project Structure

```text
global-dependency-risk-simulator/
├── models.py
├── dependency_graph.py
├── simulator.py
├── optimized_simulator.py
├── synthetic_data.py
├── sample_data.py
├── main.py
├── benchmark.py
├── benchmark_results/
│   ├── performance_results.csv
│   ├── benchmark_summary.txt
│   └── runtime_comparison.png
├── tests/
│   ├── __init__.py
│   ├── test_dependency_graph.py
│   ├── test_simulator.py
│   └── test_optimization.py
├── test_graph_manual.py
├── test_simulator_manual.py
├── report.md
├── report_deliverable3.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or later
- pytest
- matplotlib

Install project dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Main Application

Run:

```bash
python main.py
```

The application will:

1. Build the seven-entity sample graph.
2. Display the number of entities and dependencies.
3. Perform Breadth-First Search traversal.
4. Simulate a semiconductor disruption.
5. Display ranked cascading impacts.

## Running the Tests

Run:

```bash
python -m pytest -v
```

Expected result after Phase 3:

```text
24 passed
```

## Phase 3 Optimizations

### Set-Based Dependency Index

The graph continues to store complete Dependency objects in an adjacency list. A second set-based index stores target IDs for each source.

This changes duplicate-edge detection from a linear scan of the outgoing list to average O(1) set membership.

### Graph Versioning

The graph maintains a version number that increases after every entity or dependency modification.

The optimized simulator includes this number in its cache key. Therefore, changing the graph automatically prevents an outdated simulation from being reused.

### Scenario Caching

The `CachedCascadingRiskSimulator` stores completed simulations using:

- Graph version
- Starting entity
- Initial disruption strength
- Minimum impact threshold

Repeated identical requests can return stored results without performing another complete traversal.

### Synthetic Dataset Generation

The `synthetic_data.py` module creates reproducible graphs with hundreds or thousands of entities. A fixed random seed ensures that performance tests can be repeated using the same dataset structure.

## Running the Benchmark

Run:

```bash
python benchmark.py
```

The benchmark evaluates graphs containing:

- 100 entities
- 500 entities
- 1,000 entities
- 5,000 entities

Each graph is evaluated using 25 identical disruption simulations.

The script generates:

```text
benchmark_results/performance_results.csv
benchmark_results/benchmark_summary.txt
benchmark_results/runtime_comparison.png
```

## Algorithms and Complexity

### Entity Lookup

Python dictionaries provide average O(1) entity insertion and retrieval.

### Duplicate Dependency Check

The Phase 3 target-ID sets provide average O(1) duplicate checking.

### Breadth-First Search

BFS runs in:

```text
O(V + E)
```

where:

- `V` is the number of entities.
- `E` is the number of dependencies.

### Impact Ranking

Sorting impact results requires:

```text
O(V log V)
```

### Cached Simulation

The first execution still requires graph traversal. A repeated cache hit requires average O(1) dictionary lookup plus the cost of copying the result dictionary.

## Benchmark Results

The actual benchmark results are stored in:

```text
benchmark_results/performance_results.csv
```

The runtime graph is stored in:

```text
benchmark_results/runtime_comparison.png
```

## Testing Coverage

The tests validate:

- Entity insertion
- Duplicate entities
- Dependency creation
- Missing endpoints
- Dependency removal
- Entity removal
- BFS traversal
- Impact propagation
- Invalid simulation parameters
- Impact thresholds
- Ranking and summary generation
- Cache hits and misses
- Cache-result protection
- Cache invalidation after graph changes
- Graph version changes
- Duplicate dependency optimization
- Synthetic graph scaling
- Synthetic graph reproducibility
- Invalid synthetic dataset parameters

## Author

Jahnavi Dammannagari  
University of the Cumberlands  
MSCS-532 – Algorithms and Data Structures