"""Directed graph implementation for the dependency risk simulator.

The graph stores countries, industries, resources, infrastructure systems,
and services as nodes. Directed edges represent dependency relationships
between those entities.

Phase 3 adds two optimizations:

1. A set-based target index for faster duplicate dependency checks.
2. A graph version number that allows cached simulation results to become
   invalid automatically after the graph changes.
"""

from collections import deque

from models import Dependency, Entity


class DependencyGraph:
    """Store entities and directed dependency relationships.

    The graph uses an adjacency list because global dependency networks are
    generally sparse. Most entities connect to only a small portion of all
    other entities, so an adjacency list uses less memory than an adjacency
    matrix.

    Three supporting structures are maintained:

    * ``entities`` provides average O(1) entity lookup.
    * ``adjacency_list`` stores complete outgoing Dependency objects.
    * ``_adjacency_targets`` provides average O(1) duplicate-edge checks.
    """

    def __init__(self) -> None:
        """Create an empty dependency graph."""

        # Store every Entity using its unique ID as the dictionary key.
        # This avoids scanning through a list during entity lookup.
        self.entities: dict[str, Entity] = {}

        # Each source entity maps to a list of outgoing Dependency objects.
        # Lists preserve insertion order, which makes traversal predictable.
        self.adjacency_list: dict[str, list[Dependency]] = {}

        # This additional index stores only target IDs. It allows duplicate
        # dependencies to be detected in average O(1) time rather than by
        # scanning the complete outgoing dependency list.
        self._adjacency_targets: dict[str, set[str]] = {}

        # The version changes whenever the graph structure changes. Cached
        # simulations include this version in their cache key, preventing an
        # outdated result from being returned after an update.
        self._version = 0

    @property
    def version(self) -> int:
        """Return the graph's current structural version."""

        return self._version

    def add_entity(self, entity: Entity) -> None:
        """Insert a new entity into the graph.

        Args:
            entity: Entity object to add.

        Raises:
            TypeError: If the supplied value is not an Entity.
            ValueError: If the entity ID already exists.
        """

        if not isinstance(entity, Entity):
            raise TypeError(
                "Only Entity objects can be added to the graph."
            )

        # Entity IDs are dictionary keys and must remain unique. Allowing a
        # duplicate could overwrite an existing entity while leaving its
        # dependencies in an inconsistent state.
        if entity.entity_id in self.entities:
            raise ValueError(
                f"Entity '{entity.entity_id}' already exists."
            )

        self.entities[entity.entity_id] = entity
        self.adjacency_list[entity.entity_id] = []
        self._adjacency_targets[entity.entity_id] = set()

        # Every structural modification creates a new graph version.
        self._version += 1

    def get_entity(self, entity_id: str) -> Entity:
        """Retrieve an entity using its unique identifier.

        Args:
            entity_id: ID of the entity to retrieve.

        Returns:
            Matching Entity object.

        Raises:
            KeyError: If the entity does not exist.
        """

        if entity_id not in self.entities:
            raise KeyError(
                f"Entity '{entity_id}' was not found."
            )

        return self.entities[entity_id]

    def add_dependency(self, dependency: Dependency) -> None:
        """Add a directed dependency between two existing entities.

        The dependency is stored under the source entity. This direction lets
        the simulator follow outgoing edges from a disrupted entity toward
        entities that may be affected.

        Args:
            dependency: Directed Dependency object to add.

        Raises:
            TypeError: If the value is not a Dependency.
            KeyError: If either endpoint does not exist.
            ValueError: If the dependency already exists.
        """

        if not isinstance(dependency, Dependency):
            raise TypeError(
                "Only Dependency objects can be added to the graph."
            )

        if dependency.source_id not in self.entities:
            raise KeyError(
                f"Source entity '{dependency.source_id}' "
                "was not found."
            )

        if dependency.target_id not in self.entities:
            raise KeyError(
                f"Target entity '{dependency.target_id}' "
                "was not found."
            )

        # Phase 2 scanned the source's outgoing dependency list. Phase 3 uses
        # a set, making duplicate detection average O(1).
        if dependency.target_id in self._adjacency_targets[
            dependency.source_id
        ]:
            raise ValueError(
                f"Dependency from '{dependency.source_id}' "
                f"to '{dependency.target_id}' already exists."
            )

        self.adjacency_list[dependency.source_id].append(
            dependency
        )

        self._adjacency_targets[dependency.source_id].add(
            dependency.target_id
        )

        self._version += 1

    def get_dependencies(
        self,
        source_id: str,
    ) -> list[Dependency]:
        """Return outgoing dependencies for one entity.

        A copy is returned so external code cannot accidentally modify the
        graph's internal adjacency list.

        Args:
            source_id: Source entity whose dependencies are requested.

        Returns:
            List of outgoing Dependency objects.

        Raises:
            KeyError: If the source entity does not exist.
        """

        if source_id not in self.entities:
            raise KeyError(
                f"Entity '{source_id}' was not found."
            )

        return list(self.adjacency_list[source_id])

    def remove_dependency(
        self,
        source_id: str,
        target_id: str,
    ) -> None:
        """Remove one directed dependency.

        Args:
            source_id: Source entity ID.
            target_id: Target entity ID.

        Raises:
            KeyError: If the source entity or dependency does not exist.
        """

        if source_id not in self.entities:
            raise KeyError(
                f"Entity '{source_id}' was not found."
            )

        # The target index provides a quick existence check before the list is
        # rebuilt without the selected edge.
        if target_id not in self._adjacency_targets[source_id]:
            raise KeyError(
                f"Dependency from '{source_id}' "
                f"to '{target_id}' was not found."
            )

        self.adjacency_list[source_id] = [
            dependency
            for dependency in self.adjacency_list[source_id]
            if dependency.target_id != target_id
        ]

        self._adjacency_targets[source_id].remove(target_id)
        self._version += 1

    def remove_entity(self, entity_id: str) -> None:
        """Remove an entity and all connected dependencies.

        Removing an entity requires deleting:

        1. The entity record.
        2. Its outgoing dependencies.
        3. Incoming dependencies stored under other source entities.

        Args:
            entity_id: ID of the entity to remove.

        Raises:
            KeyError: If the entity does not exist.
        """

        if entity_id not in self.entities:
            raise KeyError(
                f"Entity '{entity_id}' was not found."
            )

        # Remove the entity and every dependency originating from it.
        del self.entities[entity_id]
        del self.adjacency_list[entity_id]
        del self._adjacency_targets[entity_id]

        # Incoming dependencies are stored in other adjacency lists. The set
        # index avoids rebuilding lists that do not contain the removed node.
        for source_id, dependencies in self.adjacency_list.items():
            if entity_id in self._adjacency_targets[source_id]:
                self.adjacency_list[source_id] = [
                    dependency
                    for dependency in dependencies
                    if dependency.target_id != entity_id
                ]

                self._adjacency_targets[source_id].remove(
                    entity_id
                )

        self._version += 1

    def breadth_first_traversal(
        self,
        start_id: str,
    ) -> list[str]:
        """Visit all reachable entities using Breadth-First Search.

        BFS processes direct dependencies before moving to more distant
        dependency levels.

        Args:
            start_id: Entity where traversal begins.

        Returns:
            Entity IDs in visitation order.

        Raises:
            KeyError: If the starting entity does not exist.
        """

        if start_id not in self.entities:
            raise KeyError(
                f"Entity '{start_id}' was not found."
            )

        # deque supports O(1) removal from the front. A regular list with
        # pop(0) would shift remaining elements and become less efficient.
        queue = deque([start_id])

        # The visited set prevents duplicate processing and ensures that BFS
        # terminates if the graph contains a cycle.
        visited = {start_id}

        traversal_order: list[str] = []

        while queue:
            current_id = queue.popleft()
            traversal_order.append(current_id)

            for dependency in self.adjacency_list[current_id]:
                target_id = dependency.target_id

                if target_id not in visited:
                    visited.add(target_id)
                    queue.append(target_id)

        return traversal_order

    def entity_count(self) -> int:
        """Return the current number of entities."""

        return len(self.entities)

    def dependency_count(self) -> int:
        """Return the total number of directed dependencies."""

        return sum(
            len(dependencies)
            for dependencies in self.adjacency_list.values()
        )