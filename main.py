"""Main entry point for the global dependency risk simulator."""

from sample_data import build_sample_graph
from simulator import CascadingRiskSimulator


def display_graph_summary() -> None:
    """Build the sample graph, run a disruption, and display the results."""

    graph = build_sample_graph()

    print("=" * 65)
    print("GLOBAL DEPENDENCY AND CASCADING RISK SIMULATOR")
    print("=" * 65)

    print(f"\nNumber of entities: {graph.entity_count()}")
    print(f"Number of dependencies: {graph.dependency_count()}")

    start_entity_id = "semiconductors"

    # Breadth-first traversal shows the order in which entities are reachable
    # from the initial disruption.
    traversal_order = graph.breadth_first_traversal(start_entity_id)

    print("\nReachable entities using breadth-first traversal:")
    for position, entity_id in enumerate(traversal_order, start=1):
        entity = graph.get_entity(entity_id)
        print(f"{position}. {entity.name} ({entity.entity_id})")

    simulator = CascadingRiskSimulator(
        graph=graph,
        minimum_impact=0.01,
    )

    impacts = simulator.simulate(
        start_id=start_entity_id,
        initial_impact=1.0,
    )

    print("\n" + "-" * 65)
    print("SIMULATION RESULTS")
    print("-" * 65)

    starting_entity = graph.get_entity(start_entity_id)

    print(f"\nInitial disruption: {starting_entity.name}")
    print("Initial impact: 1.0000")

    print("\nRanked cascading impacts:")

    # The summary method combines calculated impact values with readable
    # entity details such as name, type, and region.
    for rank, result in enumerate(
        simulator.summarize_impacts(impacts),
        start=1,
    ):
        print(
            f"{rank}. {result['name']}\n"
            f"   ID: {result['entity_id']}\n"
            f"   Type: {result['entity_type']}\n"
            f"   Region: {result['region']}\n"
            f"   Impact: {result['impact']:.4f}"
        )

    print("\n" + "=" * 65)


if __name__ == "__main__":
    # This condition ensures the program runs only when main.py is executed
    # directly. It will not run automatically if main.py is imported elsewhere.
    display_graph_summary()