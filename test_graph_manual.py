"""Manual demonstration of the DependencyGraph class."""

from dependency_graph import DependencyGraph
from models import Dependency, Entity


# Create an empty directed graph.
graph = DependencyGraph()

# Create sample nodes representing resources, industries, and services.
semiconductors = Entity(
    entity_id="semiconductors",
    name="Semiconductor Production",
    entity_type="resource",
    region="Global",
    criticality=1.0,
)

automotive = Entity(
    entity_id="automotive",
    name="Automobile Manufacturing",
    entity_type="industry",
    region="Global",
    criticality=0.85,
)

electronics = Entity(
    entity_id="electronics",
    name="Consumer Electronics",
    entity_type="industry",
    region="Global",
    criticality=0.90,
)

cloud = Entity(
    entity_id="cloud",
    name="Cloud Infrastructure",
    entity_type="infrastructure",
    region="Global",
    criticality=0.80,
)

# Insert the nodes into the graph before creating edges between them.
graph.add_entity(semiconductors)
graph.add_entity(automotive)
graph.add_entity(electronics)
graph.add_entity(cloud)

# Add directed edges. These relationships show which industries may be
# affected if semiconductor production is disrupted.
graph.add_dependency(
    Dependency(
        source_id="semiconductors",
        target_id="automotive",
        relationship="supplies",
        strength=0.80,
    )
)

graph.add_dependency(
    Dependency(
        source_id="semiconductors",
        target_id="electronics",
        relationship="supplies",
        strength=0.90,
    )
)

graph.add_dependency(
    Dependency(
        source_id="electronics",
        target_id="cloud",
        relationship="supports",
        strength=0.70,
    )
)

print("Number of entities:", graph.entity_count())
print("Number of dependencies:", graph.dependency_count())

print("\nEntity search result:")
print(graph.get_entity("automotive"))

print("\nDependencies from semiconductor production:")
for dependency in graph.get_dependencies("semiconductors"):
    print(dependency)

print("\nBreadth-first traversal:")
print(graph.breadth_first_traversal("semiconductors"))