"""Performance benchmark for Deliverable 3.

This script compares repeated execution of:

1. The Phase 2 CascadingRiskSimulator.
2. The Phase 3 CachedCascadingRiskSimulator.

The benchmark measures:

* Total runtime
* Peak allocated memory
* Cache-based speedup
* Entity and dependency counts

Results are written to:

* benchmark_results/performance_results.csv
* benchmark_results/runtime_comparison.png
* benchmark_results/benchmark_summary.txt
"""

import csv
import time
import tracemalloc
from pathlib import Path

from optimized_simulator import (
    CachedCascadingRiskSimulator,
)
from simulator import CascadingRiskSimulator
from synthetic_data import build_synthetic_graph


GRAPH_SIZES = (100, 500, 1000, 5000)
SIMULATION_REPETITIONS = 25
DEPENDENCIES_PER_ENTITY = 3
START_ENTITY_ID = "entity_0"
INITIAL_IMPACT = 1.0

OUTPUT_DIRECTORY = Path("benchmark_results")
CSV_PATH = (
    OUTPUT_DIRECTORY / "performance_results.csv"
)
GRAPH_PATH = (
    OUTPUT_DIRECTORY / "runtime_comparison.png"
)
SUMMARY_PATH = (
    OUTPUT_DIRECTORY / "benchmark_summary.txt"
)


def measure_simulator(
    simulator: CascadingRiskSimulator,
    repetitions: int,
) -> tuple[float, float]:
    """Measure runtime and peak allocated memory.

    Args:
        simulator: Simulator to benchmark.
        repetitions: Number of identical simulations.

    Returns:
        Total elapsed milliseconds and peak memory in KiB.
    """

    tracemalloc.start()
    start_time = time.perf_counter()

    for _ in range(repetitions):
        simulator.simulate(
            start_id=START_ENTITY_ID,
            initial_impact=INITIAL_IMPACT,
        )

    elapsed_seconds = (
        time.perf_counter() - start_time
    )

    _, peak_memory_bytes = (
        tracemalloc.get_traced_memory()
    )

    tracemalloc.stop()

    return (
        elapsed_seconds * 1000,
        peak_memory_bytes / 1024,
    )


def run_benchmarks() -> list[dict[str, int | float]]:
    """Run baseline and optimized benchmarks."""

    results: list[dict[str, int | float]] = []

    for entity_count in GRAPH_SIZES:
        print(
            f"\nBuilding graph with "
            f"{entity_count:,} entities..."
        )

        graph = build_synthetic_graph(
            entity_count=entity_count,
            dependencies_per_entity=(
                DEPENDENCIES_PER_ENTITY
            ),
            seed=42,
        )

        baseline_simulator = (
            CascadingRiskSimulator(
                graph=graph,
                minimum_impact=0.01,
            )
        )

        optimized_simulator = (
            CachedCascadingRiskSimulator(
                graph=graph,
                minimum_impact=0.01,
            )
        )

        # Warm the cache once so the optimized measurement represents repeated
        # requests rather than the initial calculation.
        optimized_simulator.simulate(
            start_id=START_ENTITY_ID,
            initial_impact=INITIAL_IMPACT,
        )

        (
            baseline_time_ms,
            baseline_memory_kib,
        ) = measure_simulator(
            simulator=baseline_simulator,
            repetitions=SIMULATION_REPETITIONS,
        )

        (
            optimized_time_ms,
            optimized_memory_kib,
        ) = measure_simulator(
            simulator=optimized_simulator,
            repetitions=SIMULATION_REPETITIONS,
        )

        if optimized_time_ms > 0:
            speedup = (
                baseline_time_ms
                / optimized_time_ms
            )
        else:
            speedup = 0.0

        row: dict[str, int | float] = {
            "entities": entity_count,
            "dependencies": (
                graph.dependency_count()
            ),
            "repetitions": (
                SIMULATION_REPETITIONS
            ),
            "baseline_time_ms": round(
                baseline_time_ms,
                4,
            ),
            "optimized_time_ms": round(
                optimized_time_ms,
                4,
            ),
            "speedup": round(
                speedup,
                2,
            ),
            "baseline_peak_memory_kib": round(
                baseline_memory_kib,
                2,
            ),
            "optimized_peak_memory_kib": round(
                optimized_memory_kib,
                2,
            ),
        }

        results.append(row)

        print(
            f"Dependencies: "
            f"{row['dependencies']:,}"
        )
        print(
            f"Baseline time: "
            f"{row['baseline_time_ms']:.4f} ms"
        )
        print(
            f"Optimized time: "
            f"{row['optimized_time_ms']:.4f} ms"
        )
        print(
            f"Speedup: "
            f"{row['speedup']:.2f}x"
        )

    return results


def save_csv(
    results: list[dict[str, int | float]],
) -> None:
    """Save benchmark results to CSV."""

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    with CSV_PATH.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=list(
                results[0].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(results)


def build_summary_text(
    results: list[dict[str, int | float]],
) -> str:
    """Create a text table for the report and README."""

    lines = [
        "PERFORMANCE SUMMARY",
        "-" * 88,
        (
            f"{'Entities':>10}"
            f"{'Edges':>12}"
            f"{'Baseline ms':>16}"
            f"{'Optimized ms':>17}"
            f"{'Speedup':>12}"
        ),
        "-" * 88,
    ]

    for result in results:
        lines.append(
            f"{result['entities']:>10,}"
            f"{result['dependencies']:>12,}"
            f"{result['baseline_time_ms']:>16.4f}"
            f"{result['optimized_time_ms']:>17.4f}"
            f"{result['speedup']:>11.2f}x"
        )

    return "\n".join(lines)


def save_summary(
    results: list[dict[str, int | float]],
) -> None:
    """Save a readable benchmark summary."""

    summary = build_summary_text(results)

    SUMMARY_PATH.write_text(
        summary + "\n",
        encoding="utf-8",
    )


def create_runtime_graph(
    results: list[dict[str, int | float]],
) -> None:
    """Generate a line graph comparing runtime."""

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print(
            "\nMatplotlib is not installed. "
            "CSV and summary files were created, "
            "but the graph was skipped."
        )
        return

    entity_counts = [
        result["entities"]
        for result in results
    ]

    baseline_times = [
        result["baseline_time_ms"]
        for result in results
    ]

    optimized_times = [
        result["optimized_time_ms"]
        for result in results
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        entity_counts,
        baseline_times,
        marker="o",
        label="Phase 2 baseline",
    )

    plt.plot(
        entity_counts,
        optimized_times,
        marker="o",
        label="Phase 3 cached",
    )

    plt.xlabel("Number of entities")
    plt.ylabel(
        f"Total time for "
        f"{SIMULATION_REPETITIONS} "
        "simulations (ms)"
    )

    plt.title(
        "Baseline and Optimized "
        "Simulation Performance"
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        GRAPH_PATH,
        dpi=200,
    )

    plt.close()


def display_summary(
    results: list[dict[str, int | float]],
) -> None:
    """Print the benchmark table."""

    print()
    print(build_summary_text(results))


def main() -> None:
    """Run all benchmarks and save the results."""

    results = run_benchmarks()

    save_csv(results)
    save_summary(results)
    create_runtime_graph(results)
    display_summary(results)

    print(
        f"\nCSV saved to: {CSV_PATH}"
    )
    print(
        f"Summary saved to: {SUMMARY_PATH}"
    )
    print(
        f"Graph saved to: {GRAPH_PATH}"
    )


if __name__ == "__main__":
    main()