"""Synthetic dependency graph generation for scalability testing.

The Phase 2 proof of concept used a small manually created graph. This module
creates larger, repeatable dependency graphs for performance and stress testing.
"""

import random

from dependency_graph import DependencyGraph
from models import Dependency, Entity


def build_synthetic_graph(
    entity_count: int,
    dependencies_per_entity: int = 3,
    seed: int = 42,
) -> DependencyGraph:
    """Create and return a repeatable synthetic dependency graph.

    Args:
        entity_count: Number of entities to create.
        dependencies_per_entity: Maximum outgoing edges for each entity.
        seed: Random seed used to reproduce the same graph.

    Returns:
        A populated DependencyGraph.

    Raises:
        ValueError: If the supplied size values are invalid.
    """

    if entity_count < 1:
        raise ValueError(
            "entity_count must be at least 1."
        )

    if dependencies_per_entity < 0:
        raise ValueError(
            "dependencies_per_entity cannot be negative."
        )

    random_generator = random.Random(seed)
    graph = DependencyGraph()

    # Create all nodes first because each dependency requires both its
    # source and target entities to already exist in the graph.
    for index in range(entity_count):
        graph.add_entity(
            Entity(
                entity_id=f"entity_{index}",
                name=f"Synthetic Entity {index}",
                entity_type="synthetic",
                region="Global",
                criticality=random_generator.uniform(
                    0.70,
                    1.00,
                ),
            )
        )

    # Connect each source only to entities with larger index values.
    # This prevents self-dependencies and creates an acyclic graph.
    for source_index in range(entity_count - 1):
        possible_targets = list(
            range(
                source_index + 1,
                entity_count,
            )
        )

        target_count = min(
            dependencies_per_entity,
            len(possible_targets),
        )

        if target_count == 0:
            continue

        selected_targets = random_generator.sample(
            possible_targets,
            k=target_count,
        )

        for target_index in selected_targets:
            graph.add_dependency(
                Dependency(
                    source_id=f"entity_{source_index}",
                    target_id=f"entity_{target_index}",
                    relationship="depends_on",
                    strength=random_generator.uniform(
                        0.50,
                        0.95,
                    ),
                )
            )

    return graph