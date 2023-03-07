
from ...._auxiliary_lib import (
    AnyTreeFastLeafIter,
    anytree_iterative_deepcopy,
    anytree_peel_sibling_to_cousin,
)
from .._impl import TrieInnerNode


def _peel_back_conjoined_leaves(
    trie: TrieInnerNode,
    p_differentia_collision: float,
    mutate: bool = False,
) -> TrieInnerNode:
    """Implementation detail for `SampleAncestralRollbacks.__call__`.

    See `SampleAncestralRollbacks.__call__` for parameter descriptions.
    """


class PeelBackConjoinedLeavesTriePostprocessor:
    def __call__(
        self: "PeelBackConjoinedLeavesTriePostprocessor",
        trie: TrieInnerNode,
        p_differentia_collision: float,
        mutate: bool = False,
    ) -> TrieInnerNode:
        """Peel apart any `TrieLeafNode` nodes that are direct siblings.

        Without reproduction dynamics that allow columns to be cloned without
        stratum deposit, two hereditary stratigraphic columns can only share
        their most-recent strata by collision.

        Clones the sibling leaves' parent node and attaches it to the
        the siblings' grandparent node. One sibling node is then grafted away
        from its original parent and attached onto the newly cloned parent node
        as a child. The original parent node is left in place with any
        remaining children. This process is repeated until no `TrieLeafNode`'s
        remain as direct siblings.

        Parameters:
        ----------
        trie : TrieInnerNode
            The root node of the trie to be unzipped.
        p_differentia_collision : float
            The multiplicative inverse of the number of possible
            differentia.

            This fraction of possible rollbacks are performed.
        mutate : bool, default False
            Are side effects on the input argument `trie` allowed?

        Returns
        -------
        TrieInnerNode
            The postprocessed trie.
        """
        if not mutate:
            trie = anytree_iterative_deepcopy(trie)

        for leaf in AnyTreeFastLeafIter(trie):
            if sum(1 for __ in leaf.parent.outer_children) > 1:
                anytree_peel_sibling_to_cousin(leaf)

        return trie
