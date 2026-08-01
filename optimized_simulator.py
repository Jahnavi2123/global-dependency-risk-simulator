"""Cached cascading risk simulator for Deliverable 3.

The Phase 2 simulator recalculates a disruption scenario every time it is
requested. This is correct, but it repeats the same graph traversal when users
run an identical scenario more than once.

This optimized simulator adds memoization. Results are cached using:

* Graph version
* Starting entity
* Initial disruption strength
* Minimum propagation threshold

Including the graph version prevents outdated cached results from being
returned after an entity or dependency is added or removed.
"""

from dependency_graph import DependencyGraph
from simulator import CascadingRiskSimulator


class CachedCascadingRiskSimulator(
    CascadingRiskSimulator
):
    """Add scenario caching to the Phase 2 simulator."""

    def __init__(
        self,
        graph: DependencyGraph,
        minimum_impact: float = 0.01,
    ) -> None:
        """Initialize the simulator and an empty result cache."""

        super().__init__(
            graph=graph,
            minimum_impact=minimum_impact,
        )

        # Cache keys describe complete simulation scenarios.
        # Cache values store the calculated impact dictionary.
        self._cache: dict[
            tuple[int, str, float, float],
            dict[str, float],
        ] = {}

        # These counters help test and demonstrate cache behavior.
        self.cache_hits = 0
        self.cache_misses = 0

    def simulate(
        self,
        start_id: str,
        initial_impact: float = 1.0,
    ) -> dict[str, float]:
        """Return a cached result or perform a new simulation.

        Args:
            start_id: Initially disrupted entity.
            initial_impact: Starting disruption strength.

        Returns:
            Mapping of entity IDs to calculated impact values.
        """

        cache_key = (
            self.graph.version,
            start_id,
            round(initial_impact, 12),
            round(self.minimum_impact, 12),
        )

        if cache_key in self._cache:
            self.cache_hits += 1

            # Return a copy so calling code cannot change the stored result.
            return dict(self._cache[cache_key])

        self.cache_misses += 1

        # Reuse the already-tested Phase 2 algorithm for the calculation.
        impacts = super().simulate(
            start_id=start_id,
            initial_impact=initial_impact,
        )

        self._cache[cache_key] = dict(impacts)

        return impacts

    def clear_cache(self) -> None:
        """Remove all stored scenarios and reset cache statistics."""

        self._cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0

    def cache_size(self) -> int:
        """Return the number of cached scenarios."""

        return len(self._cache)