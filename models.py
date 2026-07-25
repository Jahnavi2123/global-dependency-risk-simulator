"""Data models used by the global dependency risk simulator.

This module contains the basic objects that represent entities and their
dependency relationships. Keeping these models in a separate module makes
the project easier to understand and allows the graph and simulation logic
to focus only on their own responsibilities.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Entity:
    """Represent one item within the global dependency network.

    An entity can represent a resource, industry, country, infrastructure
    system, or service. Each entity has a unique identifier that is used as
    the dictionary key inside the dependency graph.

    The class is frozen because an entity's identifying information should
    not change after it has been inserted into the graph. This helps prevent
    accidental changes that could make the graph inconsistent.
    """

    entity_id: str
    name: str
    entity_type: str
    region: str
    criticality: float = 1.0

    def __post_init__(self) -> None:
        """Validate the entity immediately after it is created."""

        # The identifier is used as the dictionary key in the graph.
        # Allowing an empty identifier would make lookup and dependency
        # operations unreliable, so blank identifiers are rejected.
        if not self.entity_id.strip():
            raise ValueError("Entity ID cannot be empty.")

        # A readable name is required because simulation results are shown
        # to the user using the entity's name rather than only its ID.
        if not self.name.strip():
            raise ValueError("Entity name cannot be empty.")

        # Criticality represents how important the entity is when calculating
        # a propagated disruption. A normalized range from 0 to 1 keeps the
        # calculation predictable and prevents unrealistic impact values.
        if not 0.0 <= self.criticality <= 1.0:
            raise ValueError("Criticality must be between 0 and 1.")


@dataclass(frozen=True)
class Dependency:
    """Represent a directed relationship between two entities.

    The source entity influences the target entity. For example, if
    semiconductor production supports automobile manufacturing, the source
    is semiconductor production and the target is automobile manufacturing.
    """

    source_id: str
    target_id: str
    relationship: str
    strength: float

    def __post_init__(self) -> None:
        """Validate the dependency after it is created."""

        # Both endpoint identifiers are required because the graph must know
        # which entity supplies the dependency and which entity is affected.
        if not self.source_id.strip() or not self.target_id.strip():
            raise ValueError("Source and target IDs cannot be empty.")

        # A direct self-dependency does not provide useful information for
        # this proof of concept and could create unnecessary processing.
        if self.source_id == self.target_id:
            raise ValueError("An entity cannot directly depend on itself.")

        # The relationship description explains what the edge means, such as
        # "supplies," "powers," or "hosts."
        if not self.relationship.strip():
            raise ValueError("Dependency relationship cannot be empty.")

        # Strength controls how much of the source disruption is transferred
        # to the target. Limiting it to 0 through 1 prevents the dependency
        # from increasing the impact beyond the incoming disruption.
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("Dependency strength must be between 0 and 1.")