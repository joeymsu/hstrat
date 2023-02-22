from ..genome_instrumentation import HereditaryStratigraphicColumn


def calc_probability_differentia_collision_between(
    first: HereditaryStratigraphicColumn,
    second: HereditaryStratigraphicColumn,
) -> float:
    """How likely are differentia collisions?

    Calculates the probability of two randomly-differentiated differentia
    being identical by coincidence.
    """
    assert (
        first.GetStratumDifferentiaBitWidth()
        == second.GetStratumDifferentiaBitWidth()
    )
    return 1.0 / 2 ** first.GetStratumDifferentiaBitWidth()
