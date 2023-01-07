import itertools as it
import os
import random

import alifedata_phyloinformatics_convert as apc
import dendropy as dp
import pandas as pd
import pytest

from hstrat import hstrat

assets_path = os.path.join(os.path.dirname(__file__), "assets")


@pytest.mark.parametrize(
    "always_store_rank_in_stratum",
    [True, False],
)
@pytest.mark.parametrize(
    "num_predeposits",
    [
        0,
        1,
        10,
        100,
    ],
)
@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.nominal_resolution_algo.Policy(),
        hstrat.depth_proportional_resolution_algo.Policy(
            depth_proportional_resolution=10
        ),
        hstrat.depth_proportional_resolution_algo.Policy(
            depth_proportional_resolution=100
        ),
        pytest.param(
            hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
            marks=pytest.mark.heavy_2a,
        ),
        hstrat.recency_proportional_resolution_algo.Policy(
            recency_proportional_resolution=2
        ),
    ],
)
@pytest.mark.parametrize(
    "set_stem_length",
    [
        lambda node: 1,
        lambda node: 1 + random.randrange(10),
        pytest.param(
            lambda node: 1 + random.randrange(100),
            marks=pytest.mark.heavy_2b,
        ),
    ],
)
@pytest.mark.parametrize(
    "tree",
    [
        dp.Tree(),
        dp.Tree.get(
            path=f"{assets_path}/grandchild_and_aunt.newick", schema="newick"
        ),
        dp.Tree.get(
            path=f"{assets_path}/grandchild_and_auntuncle.newick",
            schema="newick",
        ),
        dp.Tree.get(path=f"{assets_path}/grandchild.newick", schema="newick"),
        dp.Tree.get(
            path=f"{assets_path}/grandtriplets_and_aunt.newick",
            schema="newick",
        ),
        dp.Tree.get(
            path=f"{assets_path}/grandtriplets_and_auntuncle.newick",
            schema="newick",
        ),
        dp.Tree.get(
            path=f"{assets_path}/grandtriplets.newick", schema="newick"
        ),
        dp.Tree.get(
            path=f"{assets_path}/grandtwins_and_aunt.newick", schema="newick"
        ),
        dp.Tree.get(
            path=f"{assets_path}/grandtwins_and_auntuncle.newick",
            schema="newick",
        ),
        # dp.Tree.get(path=f"{assets_path}/grandtwins.newick", schema="newick"),
        dp.Tree.get(path=f"{assets_path}/justroot.newick", schema="newick"),
        dp.Tree.get(path=f"{assets_path}/triplets.newick", schema="newick"),
        dp.Tree.get(path=f"{assets_path}/twins.newick", schema="newick"),
        apc.alife_dataframe_to_dendropy_tree(
            pd.read_csv(f"{assets_path}/nk_ecoeaselection.csv"),
        ),
        # apc.alife_dataframe_to_dendropy_tree(
        #     pd.read_csv(f"{assets_path}/nk_lexicaseselection.csv"),
        # ),
        apc.alife_dataframe_to_dendropy_tree(
            pd.read_csv(f"{assets_path}/nk_tournamentselection.csv"),
        ),
    ],
)
def test_descend_template_phylogeny_naive(
    always_store_rank_in_stratum,
    num_predeposits,
    retention_policy,
    set_stem_length,
    tree,
):
    # setup tree
    for node in tree:
        node.edge_length = set_stem_length(node)

    tree.seed_node.edge_length = num_predeposits + 1

    for idx, node in enumerate(tree.leaf_node_iter()):
        node.taxon = tree.taxon_namespace.new_taxon(label=str(idx))

    tree.update_bipartitions(
        suppress_unifurcations=False,
        collapse_unrooted_basal_bifurcation=False,
    )

    # setup seed column
    seed_column = hstrat.HereditaryStratigraphicColumn(
        stratum_retention_policy=retention_policy,
        always_store_rank_in_stratum=always_store_rank_in_stratum,
    )
    seed_column.DepositStrata(num_stratum_depositions=num_predeposits)

    extant_population = hstrat.descend_template_phylogeny_naive(
        ascending_lineage_iterators=(
            tip_node.ancestor_iter(
                inclusive=True,
            )
            for tip_node in tree.leaf_node_iter()
        ),
        descending_tree_iterator=tree.levelorder_node_iter(),
        get_parent=lambda node: node.parent_node,
        get_stem_length=lambda node: node.edge_length,
        seed_column=seed_column,
    )

    num_tips = len(tree)
    assert num_tips == len(extant_population)

    tip_depths = [
        int(tip_node.distance_from_root())
        for tip_node in tree.leaf_node_iter()
    ]
    assert tip_depths == [
        column.GetNumStrataDeposited() for column in extant_population
    ]

    assert all(
        column.GetNumStrataRetained()
        == column._stratum_retention_policy.CalcNumStrataRetainedExact(
            column.GetNumStrataDeposited()
        )
        for column in extant_population
    )
    assert all(
        a == b
        for column in extant_population
        for a, b in zip(
            column.IterRetainedRanks(),
            column._stratum_retention_policy.IterRetainedRanks(
                column.GetNumStrataDeposited()
            ),
        )
    )

    sampled_product = it.permutations(
        random.sample(
            [*zip(extant_population, tree.leaf_node_iter())],
            min(10, len(extant_population)),
        ),
        2,
    )
    spliced_product = it.permutations(
        it.islice(zip(extant_population, tree.leaf_node_iter()), 10),
        2,
    )

    for (c1, n1), (c2, n2) in it.chain(sampled_product, spliced_product):
        lb, ub = hstrat.calc_rank_of_mrca_bounds_between(c1, c2)
        mrca = tree.mrca(taxa=[n1.taxon, n2.taxon])
        assert lb <= mrca.distance_from_root() - 1 < ub
