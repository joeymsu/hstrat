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
    [
        True,
        False,
    ],
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
        hstrat.stochastic_algo.Policy(retention_probability=0.05),
        hstrat.depth_proportional_resolution_algo.Policy(
            depth_proportional_resolution=10
        ),
        hstrat.recency_proportional_resolution_algo.Policy(
            recency_proportional_resolution=2
        ),
    ],
)
@pytest.mark.parametrize(
    "phylogeny_df",
    [
        # pd.read_csv(f"{assets_path}/nk_ecoeaselection.csv"),
        # pd.read_csv(f"{assets_path}/nk_lexicaseselection.csv"),
        pd.read_csv(f"{assets_path}/nk_tournamentselection.csv"),
    ],
)
def test_descend_template_phylogeny(
    always_store_rank_in_stratum,
    num_predeposits,
    retention_policy,
    phylogeny_df,
):

    tree = apc.alife_dataframe_to_dendropy_tree(
        phylogeny_df,
        setup_edge_lengths=True,
    )

    tree.seed_node.edge_length = num_predeposits

    for node in tree:
        node.taxon = tree.taxon_namespace.new_taxon(label=node.id)

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

    sampled_tree_nodes = random.sample([*tree], 7)
    for extant_ids, sorted_extant_nodes in (
        (None, sorted(tree.leaf_node_iter(), key=lambda node: node.id)),
        (map(lambda node: node.id, sampled_tree_nodes), sampled_tree_nodes),
    ):

        extant_population = hstrat.descend_template_phylogeny_alifestd(
            phylogeny_df,
            seed_column=seed_column,
            extant_ids=extant_ids,
        )

        num_tips = len(sorted_extant_nodes)
        assert num_tips == len(extant_population)

        tip_depths = [
            int(tip_node.distance_from_root())
            for tip_node in sorted_extant_nodes
        ]
        assert tip_depths == [
            column.GetNumStrataDeposited() - 1 for column in extant_population
        ]

        sampled_product = it.permutations(
            random.sample(
                [*zip(extant_population, sorted_extant_nodes)],
                min(10, len(extant_population)),
            ),
            2,
        )
        spliced_product = it.permutations(
            it.islice(zip(extant_population, sorted_extant_nodes), 10),
            2,
        )

        for (c1, n1), (c2, n2) in it.chain(sampled_product, spliced_product):
            lb, ub = hstrat.calc_rank_of_mrca_bounds_between(c1, c2)
            assert n1 != n2
            if n1 in n2.ancestor_iter():
                mrca = n1
            elif n2 in n1.ancestor_iter():
                mrca = n2
            else:
                mrca = tree.mrca(
                    taxa=[n1.taxon, n2.taxon],
                    is_bipartitions_updated=True,
                )
                # patch for dendropy bug where internal unifurcations are not accounted
                # for in mrca detection
                # see https://github.com/jeetsukumaran/DendroPy/pull/148
                while mrca.num_child_nodes() == 1:
                    (mrca,) = mrca.child_nodes()

            assert lb <= mrca.distance_from_root() < ub
