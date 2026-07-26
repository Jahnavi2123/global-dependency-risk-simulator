"""Manual test for the cascading risk simulator."""

from dependency_graph import DependencyGraph
from models import Dependency, Entity
from simulator import CascadingRiskSimulator


graph = DependencyGraph()

# Create the entities in the sample dependency network.
entities = [
    Entity(
        entity_id="semiconductors",
        name="Semiconductor Production",
        entity_type="resource",
        region="Global",
        criticality=1.0,
    ),
    Entity(
        entity_id="automotive",
        name="Automobile Manufacturing",
        entity_type="industry",
        region="Global",
        criticality=0.85,
    ),
    Entity(
        entity_id="electronics",
        name="Consumer Electronics",
        entity_type="industry",
        region="Global",
        criticality=0.90,
    ),
    Entity(
        entity_id="cloud",
        name="Cloud Infrastructure",
        entity_type="infrastructure",
        region="Global",
        criticality=0.80,
    ),
]

for entity in entities:
    graph.add_entity(entity)

# Create directed relationships between the entities.
dependencies = [
    Dependency(
        source_id="semiconductors",
        target_id="automotive",
        relationship="supplies",
        strength=0.80,
    ),
    Dependency(
        source_id="semiconductors",
        target_id="electronics",
        relationship="supplies",
        strength=0.90,
    ),
    Dependency(
        source_id="electronics",
        target_id="cloud",
        relationship="supports",
        strength=0.70,
    ),
]

for dependency in dependencies:
    graph.add_dependency(dependency)

# Begin the disruption at semiconductor production.
simulator = CascadingRiskSimulator(
    graph=graph,
    minimum_impact=0.01,
)

impacts = simulator.simulate(
    start_id="semiconductors",
    initial_impact=1.0,
)

print("Raw impact results:")
print(impacts)

print("\nRanked impact results:")
for entity_id, impact in simulator.rank_impacts(impacts):
    print(f"{entity_id}: {impact:.4f}")

print("\nDetailed impact summary:")
for result in simulator.summarize_impacts(impacts):
    print(result)