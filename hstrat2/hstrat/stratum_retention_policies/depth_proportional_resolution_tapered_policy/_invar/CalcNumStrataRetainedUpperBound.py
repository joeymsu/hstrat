import typing

from ..PolicySpec import PolicySpec


class CalcNumStrataRetainedUpperBound:
    """Functor to provide member function implementation in Policy class."""

    def __init__(
        self: 'CalcNumStrataRetainedUpperBound',
        policy_spec: typing.Optional[PolicySpec]=None,
    ) -> None:
        pass

    def __eq__(
        self: 'CalcNumStrataRetainedUpperBound',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, self.__class__)

    def __call__(
        self: 'CalcNumStrataRetainedUpperBound',
        policy: 'Policy',
        num_strata_deposited: int,
    ) -> int:
        """At most, how many strata are retained after n deposted? Inclusive."""

        spec = policy.GetSpec()

        return min(
            spec._guaranteed_depth_proportional_resolution * 2 + 1,
            num_strata_deposited,
        )
