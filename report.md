# Design and Implementation of a Graph-Based Global Dependency and Cascading Risk Simulator Using Python

---

# Abstract

Global industries are increasingly interconnected through complex supply chains and shared infrastructure. A disruption affecting one critical resource can quickly propagate across multiple industries, resulting in widespread operational and economic consequences. Understanding these dependency relationships is essential for evaluating system resilience and identifying potential risks.

This project presents the design and implementation of a graph-based Global Dependency Risk Simulator using Python. The simulator models organizations, industries, and infrastructure components as vertices in a directed graph, while dependency relationships are represented as directed edges. Breadth-First Search (BFS) is used to traverse the dependency network, and a cascading risk algorithm estimates how disruptions spread through connected entities based on dependency strength and criticality. The project emphasizes modular software design, graph algorithms, complexity analysis, automated testing, and maintainable code organization. Comprehensive unit testing validates the correctness of graph operations and simulation logic, resulting in thirteen successful automated test cases.

---

# Introduction

Modern economies depend on highly interconnected supply chains. Manufacturing, transportation, cloud infrastructure, finance, logistics, and retail continuously rely on one another to maintain daily operations. A disruption in one critical component, such as semiconductor manufacturing, can quickly affect downstream industries that depend on those resources. Recent global events have demonstrated how shortages of raw materials, transportation delays, and infrastructure failures can create cascading effects throughout international markets.

Graph data structures provide an effective way to represent these relationships because they naturally model entities as vertices and dependencies as directed edges. Once these relationships are represented as a graph, graph traversal algorithms can be applied to analyze connectivity, identify affected entities, and simulate the spread of disruptions.

The objective of this project is to develop a Global Dependency Risk Simulator capable of modeling dependency networks and estimating how disruptions propagate through interconnected systems. The project demonstrates practical applications of graph data structures, graph traversal algorithms, algorithm complexity analysis, and object-oriented software design while reinforcing concepts studied throughout the Algorithms and Data Structures course.

---

# Project Objectives

The primary objectives of this project are to:

- Design a directed graph representing global dependency relationships.
- Implement reusable data models using Python classes.
- Support graph operations such as insertion, deletion, and traversal.
- Simulate cascading disruptions through dependency networks.
- Rank entities based on their overall impact.
- Validate correctness through automated unit testing.
- Demonstrate practical applications of graph algorithms in real-world dependency analysis.

---

# System Architecture

The application follows a modular architecture in which each module has a clearly defined responsibility.

```
                    +----------------------+
                    |    sample_data.py    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |  Dependency Graph    |
                    | (Vertices & Edges)   |
                    +----------+-----------+
                               |
              +----------------+----------------+
              |                                 |
              v                                 v
     Breadth-First Search          Cascading Risk Simulator
              |                                 |
              +----------------+----------------+
                               |
                               v
                    Ranked Impact Results
```

The project consists of the following modules:

| Module | Purpose |
|---------|---------|
| models.py | Defines Entity and Dependency data models |
| dependency_graph.py | Implements graph operations |
| simulator.py | Performs cascading risk simulation |
| sample_data.py | Builds a sample dependency network |
| main.py | Executes the complete application |
| tests/ | Contains automated unit tests |

---

# System Design

## Entity Model

Each organization, infrastructure component, or resource is represented using an Entity object containing:

- Entity identifier
- Name
- Entity type
- Geographic region
- Criticality score

The criticality score indicates the relative importance of an entity during disruption propagation.

## Dependency Model

A Dependency object represents a directed relationship between two entities.

Each dependency stores:

- Source entity
- Target entity
- Relationship type
- Dependency strength

Dependency strength represents how strongly the destination depends upon the source.

---

# Graph Representation

The project represents the dependency network using a directed graph implemented as an adjacency list.

Each entity serves as a vertex while dependencies are stored as outgoing edges.

Example:

```
Semiconductors
     |
     +--------> Electronics
                    |
                    +--------> Cloud
                    |
                    +--------> Automotive
```

## Why an Adjacency List?

An adjacency list was selected instead of an adjacency matrix for several reasons.

First, dependency networks are generally sparse because each entity depends on only a limited number of other entities. An adjacency matrix would allocate memory for every possible connection regardless of whether it exists, resulting in unnecessary space consumption.

Second, graph traversal algorithms such as Breadth-First Search operate efficiently on adjacency lists because neighboring vertices can be accessed directly without scanning unused matrix entries.

Finally, adjacency lists are easier to extend when additional entities and dependencies are introduced into the network.

---

# Algorithms Used

## Breadth-First Search (BFS)

Breadth-First Search traverses the graph level by level beginning from a selected starting entity.

The algorithm:

1. Places the starting entity into a queue.
2. Removes the next entity from the queue.
3. Visits all unvisited neighboring entities.
4. Continues until the queue becomes empty.

BFS ensures every reachable entity is visited exactly once.

### Time Complexity

**O(V + E)**

where:

- V = number of vertices
- E = number of edges

---

## Cascading Risk Simulation

The cascading simulator models how disruptions spread through dependency relationships.

The simulation begins with an initial disruption affecting one entity.

For each outgoing dependency:

```
New Impact =
Current Impact
× Dependency Strength
× Destination Criticality
```

If the calculated impact falls below a predefined threshold, propagation stops.

This approach models the natural reduction of disruption intensity while preventing unnecessary computation.

---

# Complexity Analysis

| Operation | Time Complexity |
|------------|----------------|
| Add Entity | O(1) |
| Retrieve Entity | O(1) |
| Add Dependency | O(1) |
| Remove Dependency | O(E) |
| Remove Entity | O(V + E) |
| Breadth-First Search | O(V + E) |
| Cascading Simulation | O(V + E) |
| Rank Impacts | O(V log V) |

The adjacency-list implementation provides efficient storage while maintaining excellent traversal performance.

---

# Sample Dependency Network

The demonstration network contains seven interconnected entities representing realistic industries and infrastructure components.

Entities include:

- Semiconductor Production
- Consumer Electronics
- Automotive Manufacturing
- Cloud Infrastructure
- Logistics
- Retail
- Finance

These entities are connected using directed dependencies representing supply chain and operational relationships.

Example dependency path:

```
Semiconductors
        ↓
Electronics
        ↓
Cloud Infrastructure
```

A disruption beginning at semiconductor production therefore affects electronics first before eventually reaching cloud infrastructure.

---

# Implementation

The project was implemented using object-oriented programming principles.

The Entity and Dependency classes encapsulate the data associated with vertices and edges.

The DependencyGraph class manages graph operations including insertion, deletion, neighbor retrieval, graph traversal, and graph statistics.

The CascadingRiskSimulator operates independently from the graph implementation, improving modularity and maintainability. It receives a graph object, computes cascading impacts, ranks affected entities, and generates a readable summary of simulation results.

Separating responsibilities into independent modules simplifies future enhancements while improving readability and testability.

---

# Testing and Validation

Software correctness was verified using both manual and automated testing.

Manual testing was initially performed during development to verify graph construction, traversal order, and simulation output.

Automated testing was implemented using the pytest framework.

The test suite validates:

- Entity insertion
- Duplicate entity detection
- Dependency creation
- Invalid dependency handling
- Breadth-First Search traversal
- Dependency removal
- Entity removal
- Cascading simulation
- Invalid simulation inputs
- Impact ranking
- Summary generation

A total of **13 automated unit tests** were executed successfully.

Example execution:

```
=============================
13 passed in 0.01 seconds
=============================
```

Successful execution confirms the correctness of graph operations and cascading simulation logic.

---

# Challenges Encountered

Several challenges arose during implementation.

One challenge involved designing the cascading simulation to avoid repeatedly processing entities while ensuring impacts propagated correctly throughout the graph.

Another challenge involved selecting an appropriate minimum impact threshold. Without this threshold, insignificant impacts would continue propagating unnecessarily, increasing computational cost.

Developing comprehensive unit tests also required careful consideration of both normal and exceptional scenarios, including duplicate entities, missing vertices, invalid dependencies, and incorrect simulation parameters.

Addressing these challenges improved both the robustness and maintainability of the final implementation.

---

# Future Enhancements

Although the simulator satisfies the project objectives, several enhancements could improve its capabilities.

Potential future improvements include:

- Integration with real-world supply chain datasets
- Interactive graph visualization using NetworkX and Matplotlib
- Dynamic dependency updates
- Multiple simultaneous disruptions
- Probability-based dependency modeling
- Machine learning techniques for estimating dependency strengths
- Geographic visualization of cascading disruptions
- Web-based dashboard for interactive simulation

These enhancements would make the simulator more representative of real-world dependency analysis systems.

---

# Conclusion

This project successfully demonstrates how graph data structures can be applied to model complex global dependency networks and analyze cascading disruptions. Using a directed graph implemented with an adjacency list, the application efficiently represents dependency relationships while supporting insertion, deletion, traversal, and simulation operations.

Breadth-First Search enables efficient exploration of dependency networks, while the cascading risk simulator models how disruptions propagate according to dependency strength and entity criticality. The modular architecture, object-oriented implementation, and comprehensive automated testing contribute to a maintainable and reliable software solution.

The project reinforces fundamental concepts from Algorithms and Data Structures, including graph representations, traversal algorithms, complexity analysis, software modularity, and testing. Beyond fulfilling the academic objectives of the course, it also demonstrates how graph algorithms can be applied to solve practical problems involving interconnected systems and supply chain resilience.

---

# References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.

Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2014). *Data Structures and Algorithms in Python*. John Wiley & Sons.

Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley Professional.

Python Software Foundation. (2025). *Python documentation*. https://docs.python.org/3/

pytest Development Team. (2025). *pytest documentation*. https://docs.pytest.org/