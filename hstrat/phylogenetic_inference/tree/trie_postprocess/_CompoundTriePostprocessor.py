import copy
import typing

from .._impl import TrieInnerNode


class CompoundTriePostprocessor:

    _postprocessors: typing.Iterable[typing.Callable]

    def __init__(
        self: "CompoundTriePostprocessor",
        postprocessors: typing.Iterable[typing.Callable],
    ) -> None:
        self._postprocessors = postprocessors

    def __call__(
        self: "CompoundTriePostprocessor",
        trie: TrieInnerNode,
        p_differentia_collision: float,
        mutate: bool = False,
    ) -> TrieInnerNode:
        """Apply stored postprocessors in sequence.

        Parameters
        ----------
            mutate : bool, default False
                Are side effects on the input argument `trie` allowed?

        Returns
        -------
        TrieInnerNode
            The postprocessed trie.
        """
        if not mutate:
            trie = copy.deepcopy(trie)

        for postprocessor in self._postprocessors:
            trie = postprocessor(
                trie=trie,
                p_differentia_collision=p_differentia_collision,
                mutate=True,
            )

        return trie
