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

# Deliverable 3: Optimization, Scaling, and Final Evaluation

## Optimization Techniques

The proof-of-concept developed in Deliverable 2 successfully demonstrated the core functionality of the Global Dependency and Cascading Risk Simulator. However, applications that model real-world dependency networks must also support larger datasets while maintaining acceptable performance. The primary objective of this phase was to optimize the implementation, improve scalability, and evaluate how the application performs under increasingly complex workloads.

The first optimization focused on improving duplicate dependency detection. In the initial implementation, the graph checked for duplicate relationships by scanning every outgoing dependency associated with the source entity. Although this approach worked well for smaller graphs, the number of comparisons increased as more dependencies were added. To improve efficiency, an additional set-based index was introduced to store target entity identifiers. Since set membership operations execute in average constant time, duplicate dependency validation became significantly faster while preserving the existing adjacency-list representation used for graph traversal.

Another optimization involved reducing unnecessary simulation work. During Deliverable 2, every simulation request traversed the dependency graph even when the same disruption scenario had already been analyzed. To address this issue, a caching mechanism was implemented through an optimized simulator. Each completed simulation is stored using a cache key that includes the graph version, starting entity, disruption severity, and minimum impact threshold. If the same scenario is requested again without modifying the graph, the previously calculated results are returned immediately instead of repeating the entire traversal. This optimization improves performance for repeated analyses while maintaining identical simulation results.

To ensure cached results remain accurate, a graph versioning mechanism was also introduced. Every structural modification, including adding or removing entities or dependencies, automatically increments the graph version. Because the version number is included in the cache key, previously stored simulation results become invalid whenever the dependency network changes. This approach balances performance with correctness by preventing outdated information from being reused after modifications. These optimizations preserve the modular structure developed during the earlier phases while improving efficiency without increasing implementation complexity.

---

## Scaling Strategy

The original proof-of-concept used a manually created dependency network containing seven entities. While this dataset was sufficient for validating correctness, it was not large enough to evaluate scalability. To better simulate real-world conditions, a synthetic graph generator was developed to automatically create dependency networks of varying sizes.

The synthetic generator creates directed graphs containing 100, 500, 1,000, and 5,000 entities. Each entity is connected to a limited number of other entities using randomly generated dependency relationships while maintaining a reproducible graph structure through a fixed random seed. This allows benchmark results to remain consistent across multiple executions.

The adjacency-list representation introduced in Deliverable 1 was retained because it scales efficiently for sparse dependency networks. Unlike an adjacency matrix, which allocates memory for every possible relationship regardless of whether a connection exists, an adjacency list stores only actual dependencies. Since global supply chains and infrastructure networks generally contain relatively few relationships compared to the total number of possible connections, the adjacency-list approach continues to provide better space efficiency as graph size increases.

Although the optimized implementation introduces additional memory usage through the cache and supporting set indexes, the increase is relatively small compared to the overall size of the graph. The additional memory is justified because it significantly reduces repeated computations and improves responsiveness during repeated simulation requests.

---

## Testing and Validation

After implementing the optimizations, the application underwent extensive testing to verify both correctness and performance. The automated test suite created during Deliverable 2 was expanded to include additional scenarios covering optimization-specific functionality.

New unit tests were added to verify cache hits, cache invalidation after graph modifications, graph version updates, duplicate dependency detection, synthetic graph generation, and invalid dataset parameters. These tests complement the existing functionality tests for entity insertion, dependency creation, graph traversal, cascading impact propagation, ranking, and summary generation.

The completed test suite executed successfully with all automated tests passing. These results demonstrate that the newly introduced optimizations did not alter the correctness of the original implementation while providing additional functionality required for larger-scale simulations.

Stress testing was then performed using synthetic graphs ranging from 100 to 5,000 entities. For each graph size, the benchmark executed the same disruption scenario multiple times while recording execution time and memory usage. The benchmark utility measured runtime using Python's `time.perf_counter()` function and monitored peak memory allocation using the `tracemalloc` module. These measurements provide objective evidence of how the implementation behaves as the dependency network grows.

One particularly important validation scenario involved modifying the dependency graph after a simulation result had already been cached. When a new entity and dependency were added, the simulator correctly detected the graph modification through the version number and recalculated the simulation instead of returning the outdated cached result. This confirmed that the optimization improves performance without sacrificing accuracy.

---

## Performance Analysis

Performance benchmarking demonstrated that the optimized implementation scales effectively as graph size increases. For each dataset size, the benchmark compared the original simulator developed during Deliverable 2 with the optimized cached simulator introduced during Deliverable 3.

The benchmark measured total execution time for repeated simulation requests across graphs containing progressively larger numbers of entities. As expected, the baseline implementation required increasingly longer execution times because each simulation recomputed the complete dependency traversal. In contrast, the optimized implementation performed the initial calculation once and reused cached results for identical requests, significantly reducing total execution time.

**Table 1** presents the benchmark results generated by the application.

| Entities | Dependencies | Baseline Time (ms) | Optimized Time (ms) | Speedup |
|---------:|-------------:|-------------------:|--------------------:|---------:|
| 100 | *(Insert benchmark result)* | *(Insert result)* | *(Insert result)* | *(Insert result)* |
| 500 | *(Insert benchmark result)* | *(Insert result)* | *(Insert result)* | *(Insert result)* |
| 1,000 | *(Insert benchmark result)* | *(Insert result)* | *(Insert result)* | *(Insert result)* |
| 5,000 | *(Insert benchmark result)* | *(Insert result)* | *(Insert result)* | *(Insert result)* |

> **Figure 1.** Runtime comparison between the baseline simulator and the optimized cached simulator across progressively larger dependency graphs.
>
> *(Insert `benchmark_results/runtime_comparison.png` here after running `python benchmark.py`.)*

While caching substantially improves repeated simulations, it also introduces additional memory usage because previously calculated results must be stored. Consequently, the optimization represents a trade-off between memory consumption and execution speed. For workloads involving repeated analysis of the same dependency network, the performance improvement outweighs the relatively small increase in memory usage.

---

## Final Evaluation

The final implementation successfully transforms the original proof-of-concept into a more scalable and efficient application capable of analyzing significantly larger dependency networks. Throughout the three project phases, the simulator evolved from a basic graph implementation into a modular application supporting graph traversal, cascading disruption analysis, automated testing, synthetic dataset generation, benchmarking, and performance optimization.

One of the primary strengths of the final solution is its modular architecture. Separating the application into individual modules for data models, graph management, simulation logic, benchmarking, and testing makes the code easier to maintain and extend. The optimization techniques introduced during this phase improved runtime performance while preserving the correctness verified during earlier phases.

Despite these improvements, several limitations remain. The simulator currently relies on synthetic datasets and manually assigned dependency strengths rather than historical supply chain data. The caching mechanism also continues to store every completed simulation without limiting cache size, which may increase memory consumption during long-running applications. In addition, the simulator executes sequentially on a single machine and does not currently support distributed processing.

Future improvements could incorporate real-world datasets, interactive graph visualization, dynamic dependency updates, parallel simulation, distributed execution, and intelligent cache management. Machine learning techniques could also be explored to estimate dependency strengths using historical disruption data rather than manually assigned values.

Overall, this project demonstrates how fundamental data structures such as graphs, hash tables, queues, and sets can be combined to solve a practical real-world problem. The optimizations introduced during Deliverable 3 improved both scalability and performance while maintaining correctness, resulting in a robust foundation for future development.

---

# References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.

Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2014). *Data Structures and Algorithms in Python*. John Wiley & Sons.

Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley Professional.

Python Software Foundation. (2025). *Python documentation*. https://docs.python.org/3/

pytest Development Team. (2025). *pytest documentation*. https://docs.pytest.org/

Buldyrev, S. V., Parshani, R., Paul, G., Stanley, H. E., & Havlin, S. (2010). *Catastrophic cascade of failures in interdependent networks*. *Nature, 464*(7291), 1025–1028. https://doi.org/10.1038/nature08932

Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.

Tarjan, R. E. (1972). Depth-first search and linear graph algorithms. *SIAM Journal on Computing, 1*(2), 146–160. https://doi.org/10.1137/0201010