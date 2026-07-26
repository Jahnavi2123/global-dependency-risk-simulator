"""Sample dependency network used by the application.

Keeping sample-data creation in a separate module makes the project easier
to maintain. The graph-building logic can later be replaced with data loaded
from a CSV file, database, or API without changing the simulator itself.
"""

from dependency_graph import DependencyGraph
from models import Dependency, Entity


def build_sample_graph() -> DependencyGraph:
    """Create and return a sample global dependency graph.

    The sample represents several industries, resources, and infrastructure
    systems connected through directed dependencies.

    Returns:
        A populated DependencyGraph object.
    """

    graph = DependencyGraph()

    # Each entity represents a system that may either cause or receive an
    # operational disruption. Criticality indicates how sensitive or important
    # that entity is within the simulation.
    entities = [
        Entity(
            entity_id="semiconductors",
            name="Semiconductor Production",
            entity_type="resource",
            region="Global",
            criticality=1.0,
        ),
        Entity(
            entity_id="electronics",
            name="Consumer Electronics",
            entity_type="industry",
            region="Global",
            criticality=0.90,
        ),
        Entity(
            entity_id="automotive",
            name="Automobile Manufacturing",
            entity_type="industry",
            region="Global",
            criticality=0.85,
        ),
        Entity(
            entity_id="cloud",
            name="Cloud Infrastructure",
            entity_type="infrastructure",
            region="Global",
            criticality=0.80,
        ),
        Entity(
            entity_id="logistics",
            name="Global Logistics",
            entity_type="service",
            region="Global",
            criticality=0.75,
        ),
        Entity(
            entity_id="retail",
            name="Retail Operations",
            entity_type="industry",
            region="Global",
            criticality=0.70,
        ),
        Entity(
            entity_id="finance",
            name="Digital Financial Services",
            entity_type="service",
            region="Global",
            criticality=0.88,
        ),
    ]

    # Nodes must be added before dependencies because the graph verifies that
    # both endpoints exist whenever an edge is created.
    for entity in entities:
        graph.add_entity(entity)

    # Every dependency is directed from the disrupted supplier or supporting
    # system toward the entity that may be affected.
    dependencies = [
        Dependency(
            source_id="semiconductors",
            target_id="electronics",
            relationship="supplies",
            strength=0.90,
        ),
        Dependency(
            source_id="semiconductors",
            target_id="automotive",
            relationship="supplies",
            strength=0.80,
        ),
        Dependency(
            source_id="electronics",
            target_id="cloud",
            relationship="supports",
            strength=0.70,
        ),
        Dependency(
            source_id="automotive",
            target_id="logistics",
            relationship="uses",
            strength=0.60,
        ),
        Dependency(
            source_id="cloud",
            target_id="finance",
            relationship="hosts",
            strength=0.85,
        ),
        Dependency(
            source_id="cloud",
            target_id="retail",
            relationship="supports",
            strength=0.75,
        ),
        Dependency(
            source_id="logistics",
            target_id="retail",
            relationship="delivers",
            strength=0.80,
        ),
    ]

    for dependency in dependencies:
        graph.add_dependency(dependency)

    return graph