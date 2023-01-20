import pandas as pd
from tqdm import tqdm

from ._evolve_fitness_trait_population_ import (
    _apply_island_swaps,
    _apply_mutation,
    _apply_niche_swaps,
    _do_selection,
    _get_island_id,
    _get_niche_id,
    _setup_population,
)


def evolve_fitness_trait_population(
    population_size: int = 1024,
    num_islands: int = 4,
    num_niches: int = 4,
    num_generations: int = 100,
    tournament_size: int = 4,
    p_island_migration: float = 1e-3,
    p_niche_invasion: float = 1e-4,
) -> pd.DataFrame:

    island_size = population_size // num_islands
    island_niche_size = population_size // (num_islands * num_niches)
    assert island_niche_size * num_islands * num_niches == population_size
    assert tournament_size <= island_niche_size

    pop_arr, pop_tracker = _setup_population(
        island_niche_size=island_niche_size,
        num_islands=num_islands,
        num_niches=num_niches,
    )

    for generation in tqdm(range(num_generations)):
        _apply_island_swaps(
            pop_arr,
            num_niches=num_niches,
            island_size=island_size,
            island_niche_size=island_niche_size,
            p_island_swap=p_island_migration,
        )
        _apply_niche_swaps(
            pop_arr,
            num_islands=num_islands,
            num_niches=num_niches,
            island_size=island_size,
            island_niche_size=island_niche_size,
            p_niche_swap=p_niche_invasion,
        )
        _apply_mutation(pop_arr)
        idx_selections = _do_selection(
            island_niche_size=island_niche_size,
            tournament_size=tournament_size,
            pop_arr=pop_arr,
        )

        pop_arr = pop_arr[idx_selections]
        pop_tracker.ElapseGeneration(
            idx_selections,
            pop_arr,
        )

    return pop_tracker.CompilePhylogeny(
        loc_transforms={
            "island": lambda loc: _get_island_id(loc, island_size),
            "niche": lambda loc: _get_niche_id(
                loc, island_niche_size, num_niches
            ),
        },
        progress_wrap=tqdm,
    )
