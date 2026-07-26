# Global Dependency Risk Simulator

## Overview

The Global Dependency Risk Simulator is a Python-based application that models dependencies between industries, infrastructure, and resources using a directed graph. The project simulates how disruptions in one entity can propagate through connected systems, allowing users to observe cascading impacts across a dependency network.

This project was developed as part of the MSCS-532 Algorithms and Data Structures course to demonstrate practical applications of graph data structures, graph traversal algorithms, and simulation techniques.

## Features

- Graph-based representation of global dependencies
- Add and remove entities
- Add and remove dependency relationships
- Breadth-First Search (BFS) traversal
- Cascading risk simulation
- Impact ranking
- Human-readable impact summaries
- Automated unit tests using pytest

---

## Project Structure

```
global-dependency-risk-simulator/
│
├── models.py
├── dependency_graph.py
├── simulator.py
├── sample_data.py
├── main.py
│
├── tests/
│   ├── test_dependency_graph.py
│   ├── test_simulator.py
│
├── test_graph_manual.py
├── test_simulator_manual.py
└── README.md
```

---

## Requirements

- Python 3.10 or later
- pytest

Install pytest:

```bash
pip install pytest
```

---

## Running the Program

Execute:

```bash
python main.py
```

The program will:

- Build the sample dependency network
- Display graph statistics
- Perform BFS traversal
- Simulate cascading risk
- Display ranked impacts

---

## Running Tests

Run all unit tests using:

```bash
python -m pytest -v
```

Expected output:

```
13 passed
```

---

## Algorithms Used

### Directed Graph

The dependency network is represented as a directed graph where:

- Vertices represent entities
- Directed edges represent dependencies

### Breadth-First Search (BFS)

BFS is used to traverse the dependency network level by level from a selected starting entity.

Time Complexity:

```
O(V + E)
```

where:

- V = number of entities
- E = number of dependencies

### Cascading Risk Simulation

The simulator propagates disruption through outgoing dependencies while reducing the impact according to dependency strength and entity criticality.

---

## Example Output

```
Graph Summary

Entities: 7
Dependencies: 7

BFS Traversal

semiconductors
electronics
automotive
cloud
finance
retail
logistics

Impact Ranking

semiconductors : 1.0000
electronics : 0.8100
automotive : 0.6800
cloud : 0.4536
...
```

---

## Testing

The project includes automated tests for:

- Entity management
- Dependency management
- Graph traversal
- Error handling
- Cascading simulation
- Impact ranking
- Summary generation

All tests currently pass successfully.

