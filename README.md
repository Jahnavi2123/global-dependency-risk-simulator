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
├── models.py
├── dependency_graph.py
├── simulator.py
├── sample_data.py
├── main.py
├── tests/
│   ├── __init__.py
│   ├── test_dependency_graph.py
│   └── test_simulator.py
├── test_graph_manual.py
├── test_simulator_manual.py
├── report.md
├── requirements.txt
├── .gitignore
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

## Output

=================================================================
GLOBAL DEPENDENCY AND CASCADING RISK SIMULATOR
=================================================================

Number of entities: 7
Number of dependencies: 7

Reachable entities using breadth-first traversal:
1. Semiconductor Production (semiconductors)
2. Consumer Electronics (electronics)
3. Automobile Manufacturing (automotive)
4. Cloud Infrastructure (cloud)
5. Global Logistics (logistics)
6. Digital Financial Services (finance)
7. Retail Operations (retail)

-----------------------------------------------------------------
SIMULATION RESULTS
-----------------------------------------------------------------

Initial disruption: Semiconductor Production
Initial impact: 1.0000

Ranked cascading impacts:
1. Semiconductor Production
   ID: semiconductors
   Type: resource
   Region: Global
   Impact: 1.0000
2. Consumer Electronics
   ID: electronics
   Type: industry
   Region: Global
   Impact: 0.8100
3. Automobile Manufacturing
   ID: automotive
   Type: industry
   Region: Global
   Impact: 0.6800
4. Cloud Infrastructure
   ID: cloud
   Type: infrastructure
   Region: Global
   Impact: 0.4536
5. Digital Financial Services
   ID: finance
   Type: service
   Region: Global
   Impact: 0.3393
6. Global Logistics
   ID: logistics
   Type: service
   Region: Global
   Impact: 0.3060
7. Retail Operations
   ID: retail
   Type: industry
   Region: Global
   Impact: 0.2381
   
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

