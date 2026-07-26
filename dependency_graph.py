"""Directed graph implementation for the dependency risk simulator.

The graph stores countries, industries, resources, infrastructure systems,
and services as nodes. Directed edges represent dependency relationships
between those entities.

For example:

Semiconductor Production -> Automobile Manufacturing

This means that automobile manufacturing may be affected when semiconductor
production is disrupted.
"""

from collections import deque

from models import Dependency, Entity


class DependencyGraph:
    """Store entities and directed dependency relationships.

    Two dictionaries are used:

    1. ``entities`` stores each Entity using its unique ID as the key.
       This provides average O(1) insertion and lookup.

    2. ``adjacency_list`` stores the outgoing dependencies for every entity.
       An adjacency list is suitable because a real dependency network is
       usually sparse. Most entities are connected to only a small portion
       of all other entities.
    """

    def __init__(self) -> None:
        """Create an empty dependency graph."""

        # Store entities by their unique identifiers. Using a dictionary avoids
        # scanning through a list whenever the program needs to locate an entity.
        self.entities: dict[str, Entity] = {}

        # Each key represents a source entity. Its value is a list containing
        # all directed dependencies that leave that source entity.
        self.adjacency_list: dict[str, list[Dependency]] = {}

    def add_entity(self, entity: Entity) -> None:
        """Insert a new entity into the graph.

        Args:
            entity: The Entity object that should be added.

        Raises:
            TypeError: If the supplied value is not an Entity.
            ValueError: If an entity with the same ID already exists.
        """

        # Checking the type provides a clearer error than allowing an unrelated
        # object to fail later when the code tries to access ``entity_id``.
        if not isinstance(entity, Entity):
            raise TypeError("Only Entity objects can be added to the graph.")

        # Entity IDs must remain unique because they are dictionary keys.
        # Allowing a duplicate would overwrite the original entity and could
        # leave its existing dependency edges in an inconsistent state.
        if entity.entity_id in self.entities:
            raise ValueError(
                f"Entity '{entity.entity_id}' already exists."
            )

        # Insert the entity into the dictionary for efficient lookup.
        self.entities[entity.entity_id] = entity

        # Every entity receives an empty adjacency list when it is inserted.
        # Dependencies can then be added to this list later.
        self.adjacency_list[entity.entity_id] = []

    def get_entity(self, entity_id: str) -> Entity:
        """Return an entity using its unique identifier.

        Args:
            entity_id: The ID of the entity to locate.

        Returns:
            The matching Entity object.

        Raises:
            KeyError: If the entity does not exist.
        """

        # Dictionary lookup normally takes average O(1) time, which is more
        # efficient than searching through every entity in a list.
        if entity_id not in self.entities:
            raise KeyError(f"Entity '{entity_id}' was not found.")

        return self.entities[entity_id]

    def add_dependency(self, dependency: Dependency) -> None:
        """Add a directed dependency between two existing entities.

        The dependency is stored under the source entity in the adjacency list.
        This direction is important because the simulator later follows edges
        from a disrupted source to the entities that may be affected.

        Args:
            dependency: The directed Dependency object to add.

        Raises:
            TypeError: If the supplied value is not a Dependency.
            KeyError: If either endpoint does not exist.
            ValueError: If the same directed dependency already exists.
        """

        if not isinstance(dependency, Dependency):
            raise TypeError(
                "Only Dependency objects can be added to the graph."
            )

        # Both entities must exist before an edge can connect them. This keeps
        # the graph valid and prevents dependencies from pointing to missing
        # nodes.
        if dependency.source_id not in self.entities:
            raise KeyError(
                f"Source entity '{dependency.source_id}' was not found."
            )

        if dependency.target_id not in self.entities:
            raise KeyError(
                f"Target entity '{dependency.target_id}' was not found."
            )

        # Search only the outgoing edges of the source entity. This is more
        # efficient than examining every edge in the complete graph.
        for existing_dependency in self.adjacency_list[
            dependency.source_id
        ]:
            if existing_dependency.target_id == dependency.target_id:
                raise ValueError(
                    f"Dependency from '{dependency.source_id}' "
                    f"to '{dependency.target_id}' already exists."
                )

        self.adjacency_list[dependency.source_id].append(dependency)

    def get_dependencies(self, source_id: str) -> list[Dependency]:
        """Return the outgoing dependencies of one entity.

        A copy of the list is returned so outside code cannot accidentally
        modify the graph's internal adjacency list.

        Args:
            source_id: The source entity whose dependencies are requested.

        Returns:
            A list of outgoing Dependency objects.

        Raises:
            KeyError: If the source entity does not exist.
        """

        if source_id not in self.entities:
            raise KeyError(f"Entity '{source_id}' was not found.")

        return list(self.adjacency_list[source_id])

    def remove_dependency(
        self,
        source_id: str,
        target_id: str,
    ) -> None:
        """Remove a directed dependency from the graph.

        Args:
            source_id: The ID of the source entity.
            target_id: The ID of the target entity.

        Raises:
            KeyError: If the source entity or dependency does not exist.
        """

        if source_id not in self.entities:
            raise KeyError(f"Entity '{source_id}' was not found.")

        dependencies = self.adjacency_list[source_id]

        # Build a new list that excludes the requested edge. Rebuilding the
        # list is safe because it avoids modifying a list while iterating over it.
        updated_dependencies = [
            dependency
            for dependency in dependencies
            if dependency.target_id != target_id
        ]

        # If both lists have the same size, no matching edge was removed.
        if len(updated_dependencies) == len(dependencies):
            raise KeyError(
                f"Dependency from '{source_id}' to "
                f"'{target_id}' was not found."
            )

        self.adjacency_list[source_id] = updated_dependencies

    def remove_entity(self, entity_id: str) -> None:
        """Remove an entity and every dependency connected to it.

        Removing a node requires two separate operations:

        1. Remove its outgoing dependencies by deleting its adjacency-list entry.
        2. Remove incoming dependencies stored under other source entities.

        Args:
            entity_id: The ID of the entity to remove.

        Raises:
            KeyError: If the entity does not exist.
        """

        if entity_id not in self.entities:
            raise KeyError(f"Entity '{entity_id}' was not found.")

        # Remove the node and all edges that originate from it.
        del self.entities[entity_id]
        del self.adjacency_list[entity_id]

        # Incoming edges are stored in other entities' adjacency lists.
        # Each list must therefore be checked and rebuilt without edges whose
        # target is the deleted entity.
        for source_id, dependencies in self.adjacency_list.items():
            self.adjacency_list[source_id] = [
                dependency
                for dependency in dependencies
                if dependency.target_id != entity_id
            ]

    def breadth_first_traversal(self, start_id: str) -> list[str]:
        """Visit all entities reachable from a starting entity using BFS.

        Breadth-first search processes nodes level by level. In this project,
        that means direct dependencies are visited before dependencies that
        are two or more steps away.

        Args:
            start_id: The entity where traversal begins.

        Returns:
            Entity IDs in the order they were visited.

        Raises:
            KeyError: If the starting entity does not exist.
        """

        if start_id not in self.entities:
            raise KeyError(f"Entity '{start_id}' was not found.")

        # deque supports efficient removal from the front. Using list.pop(0)
        # would require shifting the remaining elements and would be slower.
        queue = deque([start_id])

        # The set prevents the same entity from being added repeatedly. It also
        # ensures that traversal ends correctly if the graph contains a cycle.
        visited = {start_id}

        traversal_order: list[str] = []

        while queue:
            # Remove the entity that has waited in the queue the longest.
            current_id = queue.popleft()
            traversal_order.append(current_id)

            # Follow every outgoing edge from the current entity.
            for dependency in self.adjacency_list[current_id]:
                target_id = dependency.target_id

                # Add each target only once. Without this check, a cycle such as
                # A -> B -> C -> A could make traversal continue indefinitely.
                if target_id not in visited:
                    visited.add(target_id)
                    queue.append(target_id)

        return traversal_order

    def entity_count(self) -> int:
        """Return the current number of entities in the graph."""

        return len(self.entities)

    def dependency_count(self) -> int:
        """Return the total number of directed dependencies in the graph."""

        # Each adjacency-list value contains the outgoing edges of one entity.
        # Summing their lengths gives the total number of graph edges.
        return sum(
            len(dependencies)
            for dependencies in self.adjacency_list.values()
        )