"""Cascading risk simulation for the dependency graph.

The simulator begins with one disrupted entity and propagates its impact
through outgoing dependency relationships.

The impact passed to a target entity depends on:

1. The current impact on the source entity.
2. The strength of the dependency edge.
3. The criticality of the target entity.

For example, if a source has an impact of 0.80 and the dependency strength
is 0.50, the target receives a base propagated impact of 0.40 before its
criticality is considered.
"""

from collections import deque

from dependency_graph import DependencyGraph


class CascadingRiskSimulator:
    """Simulate cascading disruptions across a dependency graph."""

    def __init__(
        self,
        graph: DependencyGraph,
        minimum_impact: float = 0.01,
    ) -> None:
        """Initialize the simulator.

        Args:
            graph: The dependency graph used during the simulation.
            minimum_impact: The smallest impact value that will continue
                propagating through the network.

        Raises:
            TypeError: If graph is not a DependencyGraph.
            ValueError: If minimum_impact is outside the range 0 to 1.
        """

        if not isinstance(graph, DependencyGraph):
            raise TypeError(
                "graph must be an instance of DependencyGraph."
            )

        if not 0.0 <= minimum_impact <= 1.0:
            raise ValueError(
                "minimum_impact must be between 0.0 and 1.0."
            )

        self.graph = graph
        self.minimum_impact = minimum_impact

    def simulate(
        self,
        start_id: str,
        initial_impact: float = 1.0,
    ) -> dict[str, float]:
        """Simulate a disruption beginning at one entity.

        Breadth-first processing is used so the simulator evaluates direct
        dependencies before moving to more distant levels of the network.

        Args:
            start_id: The ID of the initially disrupted entity.
            initial_impact: Starting disruption level between 0 and 1.

        Returns:
            A dictionary mapping entity IDs to their final impact values.

        Raises:
            KeyError: If the starting entity does not exist.
            ValueError: If initial_impact is outside the range 0 to 1.
        """

        # Confirm that the starting entity exists before beginning the
        # simulation. get_entity() raises a clear KeyError when it does not.
        self.graph.get_entity(start_id)

        if not 0.0 <= initial_impact <= 1.0:
            raise ValueError(
                "initial_impact must be between 0.0 and 1.0."
            )

        # This dictionary stores the strongest impact found for every entity.
        # The starting entity receives the initial disruption directly.
        impacts: dict[str, float] = {
            start_id: initial_impact
        }

        # The queue contains entities whose outgoing dependencies still need
        # to be processed.
        queue = deque([start_id])

        while queue:
            current_id = queue.popleft()
            current_impact = impacts[current_id]

            # Examine every entity that directly depends on the current entity.
            for dependency in self.graph.get_dependencies(current_id):
                target_entity = self.graph.get_entity(
                    dependency.target_id
                )

                # The propagated impact becomes weaker as it travels through
                # the network. Dependency strength controls how much of the
                # source disruption reaches the target.
                propagated_impact = (
                    current_impact
                    * dependency.strength
                    * target_entity.criticality
                )

                # Impact values are limited to 1.0 because the simulator uses
                # a normalized scale from 0.0 to 1.0.
                propagated_impact = min(propagated_impact, 1.0)

                # Very small values are ignored. This prevents insignificant
                # effects from continuing through a long chain of dependencies.
                if propagated_impact < self.minimum_impact:
                    continue

                previous_impact = impacts.get(
                    dependency.target_id,
                    0.0,
                )

                # A target may be reachable through multiple paths. We keep the
                # strongest impact rather than adding every path together,
                # which avoids unrealistic totals greater than 1.0.
                if propagated_impact > previous_impact:
                    impacts[dependency.target_id] = propagated_impact

                    # The target is added to the queue only when its impact has
                    # increased. Its outgoing dependencies must then be
                    # recalculated using the stronger value.
                    queue.append(dependency.target_id)

        return impacts

    def rank_impacts(
        self,
        impacts: dict[str, float],
    ) -> list[tuple[str, float]]:
        """Sort simulation results from highest impact to lowest.

        Args:
            impacts: Dictionary returned by simulate().

        Returns:
            A list of entity ID and impact tuples in descending order.
        """

        return sorted(
            impacts.items(),
            key=lambda item: item[1],
            reverse=True,
        )

    def summarize_impacts(
        self,
        impacts: dict[str, float],
    ) -> list[dict[str, object]]:
        """Create a readable summary containing entity information.

        Args:
            impacts: Dictionary returned by simulate().

        Returns:
            A list of dictionaries containing the entity ID, name, region,
            type, and calculated impact.
        """

        summary: list[dict[str, object]] = []

        for entity_id, impact in self.rank_impacts(impacts):
            entity = self.graph.get_entity(entity_id)

            summary.append(
                {
                    "entity_id": entity.entity_id,
                    "name": entity.name,
                    "entity_type": entity.entity_type,
                    "region": entity.region,
                    "impact": round(impact, 4),
                }
            )

        return summary