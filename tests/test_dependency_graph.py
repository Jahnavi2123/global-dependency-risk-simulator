"""Unit tests for the DependencyGraph class."""

import pytest

from dependency_graph import DependencyGraph
from models import Dependency, Entity


def create_sample_graph() -> DependencyGraph:
    """Create a small graph that can be reused by multiple tests."""

    graph = DependencyGraph()

    graph.add_entity(
        Entity(
            entity_id="semiconductors",
            name="Semiconductor Production",
            entity_type="resource",
            region="Global",
            criticality=1.0,
        )
    )

    graph.add_entity(
        Entity(
            entity_id="electronics",
            name="Consumer Electronics",
            entity_type="industry",
            region="Global",
            criticality=0.90,
        )
    )

    graph.add_entity(
        Entity(
            entity_id="cloud",
            name="Cloud Infrastructure",
            entity_type="infrastructure",
            region="Global",
            criticality=0.80,
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

    return graph


def test_add_entity() -> None:
    """Verify that an entity is successfully added to the graph."""

    graph = DependencyGraph()

    entity = Entity(
        entity_id="energy",
        name="Energy Supply",
        entity_type="resource",
        region="Global",
        criticality=0.95,
    )

    graph.add_entity(entity)

    assert graph.entity_count() == 1
    assert graph.get_entity("energy") == entity


def test_duplicate_entity_raises_error() -> None:
    """Verify that duplicate entity IDs are rejected."""

    graph = DependencyGraph()

    entity = Entity(
        entity_id="energy",
        name="Energy Supply",
        entity_type="resource",
        region="Global",
        criticality=0.95,
    )

    graph.add_entity(entity)

    with pytest.raises(ValueError):
        graph.add_entity(entity)


def test_add_dependency() -> None:
    """Verify that a directed dependency is stored correctly."""

    graph = create_sample_graph()

    dependencies = graph.get_dependencies("semiconductors")

    assert len(dependencies) == 1
    assert dependencies[0].target_id == "electronics"
    assert dependencies[0].strength == 0.90


def test_dependency_requires_existing_entities() -> None:
    """Verify that edges cannot point to missing entities."""

    graph = DependencyGraph()

    graph.add_entity(
        Entity(
            entity_id="energy",
            name="Energy Supply",
            entity_type="resource",
            region="Global",
            criticality=0.95,
        )
    )

    dependency = Dependency(
        source_id="energy",
        target_id="missing",
        relationship="supports",
        strength=0.70,
    )

    with pytest.raises(KeyError):
        graph.add_dependency(dependency)


def test_breadth_first_traversal() -> None:
    """Verify that BFS visits reachable entities level by level."""

    graph = create_sample_graph()

    traversal = graph.breadth_first_traversal("semiconductors")

    assert traversal == [
        "semiconductors",
        "electronics",
        "cloud",
    ]


def test_remove_dependency() -> None:
    """Verify that a dependency can be removed."""

    graph = create_sample_graph()

    graph.remove_dependency(
        source_id="semiconductors",
        target_id="electronics",
    )

    assert graph.get_dependencies("semiconductors") == []
    assert graph.dependency_count() == 1


def test_remove_entity_removes_connected_edges() -> None:
    """Verify that deleting an entity also removes connected edges."""

    graph = create_sample_graph()

    graph.remove_entity("electronics")

    assert graph.entity_count() == 2
    assert graph.dependency_count() == 0

    with pytest.raises(KeyError):
        graph.get_entity("electronics")