"""Unit tests for the CascadingRiskSimulator class."""

import pytest

from dependency_graph import DependencyGraph
from models import Dependency, Entity
from simulator import CascadingRiskSimulator


def create_simulation_graph() -> DependencyGraph:
    """Create a predictable graph for simulator testing."""

    graph = DependencyGraph()

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
            entity_id="cloud",
            name="Cloud Infrastructure",
            entity_type="infrastructure",
            region="Global",
            criticality=0.80,
        ),
    ]

    for entity in entities:
        graph.add_entity(entity)

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


def test_simulation_propagates_impact() -> None:
    """Verify that impact moves through the dependency chain."""

    graph = create_simulation_graph()
    simulator = CascadingRiskSimulator(graph)

    impacts = simulator.simulate(
        start_id="semiconductors",
        initial_impact=1.0,
    )

    assert impacts["semiconductors"] == 1.0
    assert impacts["electronics"] == pytest.approx(0.81)
    assert impacts["cloud"] == pytest.approx(0.4536)


def test_invalid_initial_impact_raises_error() -> None:
    """Verify that impact must remain between zero and one."""

    graph = create_simulation_graph()
    simulator = CascadingRiskSimulator(graph)

    with pytest.raises(ValueError):
        simulator.simulate(
            start_id="semiconductors",
            initial_impact=1.5,
        )


def test_missing_start_entity_raises_error() -> None:
    """Verify that simulation cannot start from a missing entity."""

    graph = create_simulation_graph()
    simulator = CascadingRiskSimulator(graph)

    with pytest.raises(KeyError):
        simulator.simulate(
            start_id="missing",
            initial_impact=1.0,
        )


def test_minimum_impact_threshold() -> None:
    """Verify that weak impacts below the threshold are ignored."""

    graph = create_simulation_graph()

    simulator = CascadingRiskSimulator(
        graph=graph,
        minimum_impact=0.50,
    )

    impacts = simulator.simulate(
        start_id="semiconductors",
        initial_impact=1.0,
    )

    assert "electronics" in impacts
    assert "cloud" not in impacts


def test_rank_impacts() -> None:
    """Verify that results are ordered from highest to lowest."""

    graph = create_simulation_graph()
    simulator = CascadingRiskSimulator(graph)

    impacts = simulator.simulate("semiconductors")

    ranked = simulator.rank_impacts(impacts)

    assert ranked[0] == ("semiconductors", 1.0)
    assert ranked[1][0] == "electronics"
    assert ranked[2][0] == "cloud"


def test_summary_contains_entity_details() -> None:
    """Verify that the summary includes readable entity information."""

    graph = create_simulation_graph()
    simulator = CascadingRiskSimulator(graph)

    impacts = simulator.simulate("semiconductors")
    summary = simulator.summarize_impacts(impacts)

    assert summary[0]["entity_id"] == "semiconductors"
    assert summary[0]["name"] == "Semiconductor Production"
    assert summary[0]["impact"] == 1.0