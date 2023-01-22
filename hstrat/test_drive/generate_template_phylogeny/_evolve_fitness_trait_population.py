import typing

import numpy as np
import pandas as pd
from tqdm import tqdm

from ..perfect_tracking import GarbageCollectingPhyloTracker
from ._evolve_fitness_trait_population_ import (
    _apply_island_migrations,
    _apply_mutation,
    _apply_niche_invasions,
    _get_island_id,
    _get_niche_id,
    _select_parents,
)


def evolve_fitness_trait_population(
    population_size: int = 1024,
    num_islands: int = 4,
    num_niches: int = 4,
    num_generations: int = 100,
    tournament_size: int = 4,
    p_island_migration: float = 1e-3,
    p_niche_invasion: float = 1e-4,
    mut_distn: typing.Callable = np.random.standard_normal,
    progress_wrap: typing.Callable = lambda x: x,
) -> pd.DataFrame:
    """Run simple evolutionary simulation to generate sample phylogeny.

    Organisms are simulated with a genetic trait, which directly corresponds to
    fitness. Mutations to this genetic trait are performed every generation.
    Tournament selection determines the composition of synchronous generations.
    One tournament is held for each slot within the upcoming generation, and
    the organism within a tournament with the highest genetic trait value is
    selected as the asexual parent of the organism to be placed in that slot.

    A simple island model allows incorporation of spatial structure into the
    simulation. Islands are arranged in a ring topology. Population size is
    evenly distributed across islands. In selection tournaments, organisms only
    compete against other organisms from the same island.

    Organisms migrate to either neighboring island with fixed per-organism per-
    generation probability. To maintain exactly fixed per-island population
    size, a copy of the migrating organism remains on the original island and
    an additional copy is placed on the target island, overwriting an
    inhabitant of that island. Care is taken such that the net number of
    migrations per generation corresponds to a binomial distribution with `n =
    population_size` and `p = p_island_migration`. A single organism may
    yield up to two migrant copies within a single generation (one migrating to
    each island). Migrant copies cannot yield further migrant copies within the
    same generation.

    A simple niche model allows incorporation of ecological dynamics into the
    simulation. A fixed number of niches are instantiated. In selection
    tournaments, organisms only compete against other organisms in the same
    niche. Islands' population capacity is evenly split between niches. That is,
    each niche hosts the same number of members within an island.

    Organisms switch to another niche ("invade" that niche) with fixed per-
    organism per-generation probabilty. The switched-to niche is determined
    randomly with all other niches having uniform probability of being chosen.
    To maintain exactly fixed niche population size, a copy of the invading
    organism remains in the original niche and an additional copy is created as
    a member of the invaded niche, overriding an existing member of the invaded
    niche. Care is taken such that the net number of niche invasions per
    generation corresponds to a binomial distribution with `n =
    population_size` and `p = p_niche_invasion`. A single organism may yield up
    to one invading copy per non-self niche available.

    Parameters
    ----------
    population_size : int, default 1024
        Number of organisms within each generational cohort.
    num_islands : int, default 4
        Must evenly divide `population_size`.
    num_niches : int, default 4
        Must evenly divide `population_size`.
    num_generations : int, default 100
        Number of generations to simulate
    tournament_size : int, default 4
        Number of organisms sampled to compete for each population slot.

        Higher `tournament_size` increases selection pressure. If set to 1,
        selection constitutes neutral drift.
    p_island_migration : float, default 1e-3
        Per-organism, per-generation probability of copying an organism into a
        neighboring island.
    p_niche_invasion : float, default 1e-4
        Per-organism, per-generation probability of copying an organism into a
        neighboring island.
    mut_distn : typing.Callable, default numpy.random.standard_normal
        Callable to generate mutation deltas applied to each organism at each
        generation.

        Must take int value `size` as sole kwarg. Must return a `numpy.array`
        of float with length `size`.
    progress_wrap : Callable, default identity function
        Wrapper applied around generation iterator; pass tqdm or equivalent to
        display progress bar for compilation process.

    Returns
    -------
    pandas.DataFrame
        Full phylogenetic record of extant organisms at end of evolutionary
        simulation in alife standard format.

    Notes
    -----
    The product of `num_islands` and `num_niches` must divide
    `population_size`.
    """

    island_size = population_size // num_islands
    island_niche_size = population_size // (num_islands * num_niches)
    assert island_niche_size * num_islands * num_niches == population_size
    assert tournament_size <= island_niche_size

    pop_arr = np.zeros(population_size, dtype=np.single)
    pop_tracker = GarbageCollectingPhyloTracker(pop_arr)

    for __ in progress_wrap(range(num_generations)):
        _apply_island_migrations(
            pop_arr,
            pop_tracker,
            num_niches=num_niches,
            island_size=island_size,
            island_niche_size=island_niche_size,
            p_island_migration=p_island_migration,
        )
        _apply_niche_invasions(
            pop_arr,
            pop_tracker,
            num_islands=num_islands,
            num_niches=num_niches,
            island_size=island_size,
            island_niche_size=island_niche_size,
            p_niche_invasion=p_niche_invasion,
        )
        _apply_mutation(pop_arr, mut_distn)
        parent_locs = _select_parents(
            island_niche_size=island_niche_size,
            tournament_size=tournament_size,
            pop_arr=pop_arr,
        )

        pop_arr = pop_arr[parent_locs]
        pop_tracker.ElapseGeneration(
            parent_locs,
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
