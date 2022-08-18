import typing

from .....helpers import memoize_generator
from ..PolicySpec import PolicySpec
from .._impl import get_retained_ranks


class IterRetainedRanks:
    """Functor to provide member function implementation in Policy class."""

    def __init__(
        self: 'IterRetainedRanks',
        policy_spec: typing.Optional[PolicySpec],
    ) -> None:
        pass

    def __hash__(self: 'IterRetainedRanks') -> int:
        """Hash object instance."""

        return 0

    def __eq__(
        self: 'IterRetainedRanks',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, self.__class__)

    @memoize_generator()
    def __call__(
        self: 'IterRetainedRanks',
        policy: 'Policy',
        num_strata_deposited: int,
    ) -> typing.Iterator[int]:
        """Iterate over retained strata ranks at `num_strata_deposited` in
        ascending order."""

        spec = policy.GetSpec()

        yield from sorted(get_retained_ranks(
            policy,
            num_strata_deposited,
        ))
