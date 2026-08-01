"""Tests for Phase 3 optimization and scaling features."""

import pytest

from dependency_graph import DependencyGraph
from models import Dependency, Entity
from optimized_simulator import (
    CachedCascadingRiskSimulator,
)
from synthetic_data import build_synthetic_graph


def build_small_graph() -> DependencyGraph:
    """Create a small deterministic graph."""

    graph = DependencyGraph()

    graph.add_entity(
        Entity(
            entity_id="energy",
            name="Energy Supply",
            entity_type="resource",
            region="Global",
            criticality=1.0,
        )
    )

    graph.add_entity(
        Entity(
            entity_id="cloud",
            name="Cloud Infrastructure",
            entity_type="infrastructure",
            region="Global",
            criticality=0.8,
        )
    )

    graph.add_dependency(
        Dependency(
            source_id="energy",
            target_id="cloud",
            relationship="powers",
            strength=0.9,
        )
    )

    return graph


def test_repeated_simulation_uses_cache() -> None:
    """An identical second request should become a cache hit."""

    graph = build_small_graph()

    simulator = CachedCascadingRiskSimulator(
        graph
    )

    first_result = simulator.simulate(
        "energy"
    )

    second_result = simulator.simulate(
        "energy"
    )

    assert first_result == second_result
    assert simulator.cache_misses == 1
    assert simulator.cache_hits == 1
    assert simulator.cache_size() == 1


def test_cached_result_is_returned_as_copy() -> None:
    """External changes must not modify the stored cache value."""

    graph = build_small_graph()

    simulator = CachedCascadingRiskSimulator(
        graph
    )

    first_result = simulator.simulate(
        "energy"
    )

    first_result["cloud"] = 999.0

    second_result = simulator.simulate(
        "energy"
    )

    assert second_result["cloud"] != 999.0


def test_graph_change_invalidates_cache() -> None:
    """Changing the graph should force a new calculation."""

    graph = build_small_graph()

    simulator = CachedCascadingRiskSimulator(
        graph
    )

    simulator.simulate("energy")

    graph.add_entity(
        Entity(
            entity_id="finance",
            name="Financial Services",
            entity_type="service",
            region="Global",
            criticality=0.85,
        )
    )

    graph.add_dependency(
        Dependency(
            source_id="cloud",
            target_id="finance",
            relationship="hosts",
            strength=0.75,
        )
    )

    updated_result = simulator.simulate(
        "energy"
    )

    assert "finance" in updated_result
    assert simulator.cache_misses == 2


def test_different_severity_uses_new_cache_entry() -> None:
    """Different initial impacts represent different scenarios."""

    graph = build_small_graph()

    simulator = CachedCascadingRiskSimulator(
        graph
    )

    simulator.simulate(
        start_id="energy",
        initial_impact=1.0,
    )

    simulator.simulate(
        start_id="energy",
        initial_impact=0.5,
    )

    assert simulator.cache_misses == 2
    assert simulator.cache_size() == 2


def test_clear_cache() -> None:
    """clear_cache should remove values and reset statistics."""

    graph = build_small_graph()

    simulator = CachedCascadingRiskSimulator(
        graph
    )

    simulator.simulate("energy")
    simulator.simulate("energy")

    simulator.clear_cache()

    assert simulator.cache_size() == 0
    assert simulator.cache_hits == 0
    assert simulator.cache_misses == 0


def test_graph_version_changes_after_update() -> None:
    """The graph version should increase after modifications."""

    graph = DependencyGraph()
    initial_version = graph.version

    graph.add_entity(
        Entity(
            entity_id="energy",
            name="Energy",
            entity_type="resource",
            region="Global",
            criticality=1.0,
        )
    )

    assert graph.version > initial_version


def test_duplicate_dependency_is_rejected() -> None:
    """The set index should reject duplicate edges."""

    graph = build_small_graph()

    with pytest.raises(ValueError):
        graph.add_dependency(
            Dependency(
                source_id="energy",
                target_id="cloud",
                relationship="powers",
                strength=0.9,
            )
        )


def test_synthetic_graph_has_requested_size() -> None:
    """Synthetic generation should create the requested nodes."""

    graph = build_synthetic_graph(
        entity_count=1000,
        dependencies_per_entity=3,
        seed=42,
    )

    assert graph.entity_count() == 1000
    assert graph.dependency_count() > 0


def test_synthetic_graph_is_reproducible() -> None:
    """The same seed should create the same graph size."""

    first_graph = build_synthetic_graph(
        entity_count=100,
        dependencies_per_entity=3,
        seed=42,
    )

    second_graph = build_synthetic_graph(
        entity_count=100,
        dependencies_per_entity=3,
        seed=42,
    )

    assert (
        first_graph.dependency_count()
        == second_graph.dependency_count()
    )

    assert (
        first_graph.get_dependencies("entity_0")
        == second_graph.get_dependencies("entity_0")
    )


def test_synthetic_graph_rejects_zero_entities() -> None:
    """An empty synthetic graph request should be rejected."""

    with pytest.raises(ValueError):
        build_synthetic_graph(
            entity_count=0
        )


def test_synthetic_graph_rejects_negative_edges() -> None:
    """A negative outgoing-edge count should be rejected."""

    with pytest.raises(ValueError):
        build_synthetic_graph(
            entity_count=100,
            dependencies_per_entity=-1,
        )