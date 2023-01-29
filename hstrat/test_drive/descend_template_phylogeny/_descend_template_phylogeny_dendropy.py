import typing

import dendropy as dp
import opytional as opyt
import ordered_set as ods
import pandas as pd

from ..._auxiliary_lib import (
    alifestd_find_leaf_ids,
    alifestd_is_disconnected,
    alifestd_is_topologically_sorted,
    alifestd_parse_ancestor_id,
    alifestd_topological_sort,
)
from ...genome_instrumentation import HereditaryStratigraphicColumn
from ._descend_template_phylogeny import descend_template_phylogeny


def descend_template_phylogeny_dendropy(
    tree: dp.Tree,
    seed_column: HereditaryStratigraphicColumn,
    extant_nodes: typing.Optional[typing.Iterable[int]] = None,
) -> typing.List[HereditaryStratigraphicColumn]:
    """Generate a population of hereditary stratigraphic columns that could
    have resulted from the template phylogeny.

    Parameters
    ----------
    tree : dendropy.Tree
        Phylogeny record as an dendropy Tree.
    seed_column : HereditaryStratigraphicColumn
        Hereditary stratigraphic column to seed at root node of phylogeny.

        Returned hereditary stratigraphic column population will be generated
        as if repeatedly calling `CloneDescendant()` on `seed_column`. As such,
        specifies configuration (i.e., differentia bit width and stratum
        retention policy) for returned columns. May already have strata
        deposited, which will be incorporated into generated extant population.
    extant_nodess : optional list of dendropy.Nonde
        Which organisms should hereditary stratigraphic columns be created for?

        Designates content and order of returned list of hereditary
        stratigraphic column.

        If None, hereditary stratigraphic columns will be created for all
        phylogenetic leaves (organisms without offspring) in order of
        appearance in `tree.leaf_node_iter()`.

    Returns
    -------
    list of HereditaryStratigraphicColumn
        Population of hereditary stratigraphic columns for extant lineage
        members (i.e., phylogeny leaf nodes).

        Columns ordered in order of appearance of corresponding extant organism
        id.
    """

    return descend_template_phylogeny(
        ascending_lineage_iterators=(
            extant_node.ancestor_iter(
                inclusive=True,
            )
            for extant_node in opyt.or_value(
                extant_nodes, tree.leaf_node_iter()
            )
        ),
        descending_tree_iterator=tree.levelorder_node_iter(),
        get_parent=lambda node: node.parent_node,
        get_stem_length=lambda node: node.edge_length,
        seed_column=seed_column,
    )
