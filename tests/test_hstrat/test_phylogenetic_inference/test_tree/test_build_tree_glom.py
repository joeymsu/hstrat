import itertools as it
import os
import random
import warnings

from Bio.Phylo.TreeConstruction import BaseTree, DistanceMatrix
import _impl as impl
import alifedata_phyloinformatics_convert as apc
import dendropy as dp
import pytest

from hstrat import hstrat
from hstrat._auxiliary_lib import alifestd_validate

assets_path = os.path.join(os.path.dirname(__file__), "assets")


# @pytest.mark.parametrize(
#     "version_pin",
#     [hstrat.__version__],
# )
# def test_empty_population(version_pin):
#     population = []
#     tree = hstrat.build_tree(
#         [],
#         version_pin=version_pin,
#     )
#
#     assert len(tree) == 0
#     assert alifestd_validate(tree)
#
#
# @pytest.mark.parametrize(
#     "version_pin",
#     [hstrat.__version__],
# )
# def test_dual_population_no_mrca(version_pin):
#     organism1 = hstrat.HereditaryStratigraphicColumn().CloneNthDescendant(100)
#     organism2 = hstrat.HereditaryStratigraphicColumn().CloneNthDescendant(100)
#
#     population = [organism1, organism2]
#     names = ["foo", "bar"]
#
#     with pytest.raises(ValueError):
#         tree = hstrat.build_tree(population, version_pin, taxon_labels=names)
#
#     tree = hstrat.build_tree(
#         population, version_pin, taxon_labels=names, force_common_ancestry=True
#     )
#     assert alifestd_validate(tree)
#
#     root_clade = BaseTree.Clade(name="Inner1")
#     root_clade.clades = [
#         BaseTree.Clade(branch_length=101.0, name="bar"),
#         BaseTree.Clade(branch_length=101.0, name="foo"),
#     ]
#     true_tree = BaseTree.Tree(rooted=False, root=root_clade)
#
#     assert (
#         impl.tree_distance_metric(
#             apc.alife_dataframe_to_biopython_tree(tree), true_tree
#         )
#         == 0.0
#     )
#
#
# @pytest.mark.parametrize(
#     "version_pin",
#     [hstrat.__version__],
# )
# def test_dual_population_with_mrca(version_pin):
#     organism1 = hstrat.HereditaryStratigraphicColumn()
#     organism2 = hstrat.HereditaryStratigraphicColumn()
#
#     population = [organism1, organism2]
#     names = ["foo", "bar"]
#
#     for _ in range(100):
#         parents = random.choices(population, k=len(population))
#         population = [parent.CloneDescendant() for parent in parents]
#
#     tree = hstrat.build_tree(
#         population, version_pin=version_pin, taxon_labels=names
#     )
#     assert alifestd_validate(tree)
#
#     root_clade = BaseTree.Clade(name="Inner")
#     root_clade.clades = [
#         BaseTree.Clade(branch_length=0.0, name="bar"),
#         BaseTree.Clade(branch_length=0.0, name="foo"),
#     ]
#     true_tree = BaseTree.Tree(rooted=False, root=root_clade)
#
#     assert (
#         impl.tree_distance_metric(
#             apc.alife_dataframe_to_biopython_tree(tree),
#             true_tree,
#         )
#         == 0.0
#     )
#
#
@pytest.mark.parametrize(
    "version_pin",
    [hstrat.__version__],
)
@pytest.mark.parametrize(
    "orig_tree",
    [
        # impl.setup_dendropy_tree(f"{assets_path}/grandchild_and_aunt.newick"),
        # impl.setup_dendropy_tree(
        #     f"{assets_path}/grandchild_and_auntuncle.newick"
        # ),
        # TODO: handle this edge case
        # impl.setup_dendropy_tree(
        #     f"{assets_path}/grandchild.newick"
        # ),
        # impl.setup_dendropy_tree(
        #     f"{assets_path}/grandtriplets_and_aunt.newick"
        # ),
        impl.setup_dendropy_tree(
            f"{assets_path}/grandtriplets_and_auntuncle.newick"
        ),
        # impl.setup_dendropy_tree(f"{assets_path}/grandtriplets.newick"),
        # impl.setup_dendropy_tree(f"{assets_path}/grandtwins_and_aunt.newick"),
        impl.setup_dendropy_tree(
            f"{assets_path}/grandtwins_and_auntuncle.newick"
        ),
        # impl.setup_dendropy_tree(f"{assets_path}/grandtwins.newick"),
        # TODO: handle this edge case
        # impl.setup_dendropy_tree(
        #     f"{assets_path}/justroot.newick"
        # ),
        # impl.setup_dendropy_tree(f"{assets_path}/triplets.newick"),
        # impl.setup_dendropy_tree(f"{assets_path}/twins.newick"),
    ],
)
def test_handwritten_trees(version_pin, orig_tree):
    extant_population = hstrat.descend_template_phylogeny_dendropy(
        orig_tree,
        seed_column=hstrat.HereditaryStratigraphicColumn().CloneNthDescendant(
            10
        ),
    )

    reconst_df = hstrat.build_tree_glom(extant_population)

    # assert alifestd_validate(reconst_df)
    # print(reconst_df)
    # # print(alifestd
    # reconst_tree = apc.alife_dataframe_to_dendropy_tree(
    #     reconst_df,
    #     setup_edge_lengths=True,
    # )
    # reconst_tree.collapse_unweighted_edges()
    #
    # common_namespace = dp.TaxonNamespace()
    # orig_tree.migrate_taxon_namespace(common_namespace)
    # reconst_tree.migrate_taxon_namespace(common_namespace)
    #
    # original_distance_matrix = orig_tree.phylogenetic_distance_matrix()
    # reconstructed_distance_matrix = reconst_tree.phylogenetic_distance_matrix()
    #
    # taxa = [node.taxon for node in orig_tree.leaf_node_iter()]
    #
    # for a, b in it.combinations(taxa, 2):
    #     assert (
    #         abs(
    #             original_distance_matrix.distance(a, b)
    #             - reconstructed_distance_matrix.distance(a, b)
    #         )
    #         < 2.0
    #     )
    #
    # assert impl.tree_distance_metric(orig_tree, reconst_tree) < 2.0
    #
    #


@pytest.mark.parametrize(
    "orig_tree",
    [
        # TODO
        # pytest.param(
        #     impl.setup_dendropy_tree(f"{assets_path}/nk_ecoeaselection.csv"),
        #     marks=pytest.mark.heavy,
        # ),

        impl.setup_dendropy_tree(f"{assets_path}/nk_lexicaseselection.csv"),
        # impl.setup_dendropy_tree(f"{assets_path}/nk_tournamentselection.csv"),
    ],
)
# @pytest.mark.parametrize(
#     "retention_policy",
#     [
#       TODO
#     ]
# )
def test_reconstructed_mrca(orig_tree):
    num_depositions = 10

    extant_population = hstrat.descend_template_phylogeny_dendropy(
        orig_tree,
        seed_column=hstrat.HereditaryStratigraphicColumn().CloneNthDescendant(
            num_depositions
        ),
    )

    reconst_df = hstrat.build_tree_glom(extant_population)
    reconst_df["taxon_label"] = reconst_df["id"]
    assert "origin_time" in reconst_df

    assert alifestd_validate(reconst_df)
    reconst_tree = apc.alife_dataframe_to_dendropy_tree(
        reconst_df,
        setup_edge_lengths=True,
    )
    pdm = reconst_tree.phylogenetic_distance_matrix()

    assert len(list(reconst_tree.leaf_node_iter())) == len(extant_population)
    sorted_leaf_nodes = sorted(
        reconst_tree.leaf_node_iter(), key=lambda x: int(x.taxon.label)
    )
    assert {
        int(leaf_node.distance_from_root()) for leaf_node in sorted_leaf_nodes
    } == {
        extant_col.GetNumStrataDeposited() - 1
        for extant_col in extant_population
    }
    assert sorted(
        int(leaf_node.distance_from_root()) for leaf_node in sorted_leaf_nodes
    ) == sorted(
        extant_col.GetNumStrataDeposited() - 1
        for extant_col in extant_population
    )
    assert [
        int(leaf_node.distance_from_root()) for leaf_node in sorted_leaf_nodes
    ] == [
        extant_col.GetNumStrataDeposited() - 1
        for extant_col in extant_population
    ]

    good = 0
    total = 0
    for reconst_node_pair, extant_column_pair in zip(
        it.combinations(sorted_leaf_nodes, 2),
        it.combinations(extant_population, 2),
    ):
        reconst_mrca = impl.descend_unifurcations(
            pdm.mrca(*map(lambda x: x.taxon, reconst_node_pair))
        )

        (
            lower_mrca_bound,
            upper_mrca_bound,
        ) = hstrat.calc_rank_of_mrca_bounds_between(
            *extant_column_pair, prior="arbitrary"
        )

        good += (
            lower_mrca_bound
            <= reconst_mrca.distance_from_root()
            < upper_mrca_bound
        )
        total += 1

    print(good, total)


# # TODO test determinism
