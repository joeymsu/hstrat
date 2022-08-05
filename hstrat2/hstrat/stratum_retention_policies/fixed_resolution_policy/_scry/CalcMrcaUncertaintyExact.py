import typing

from ..PolicySpec import PolicySpec

class CalcMrcaUncertaintyExact:
    """Functor to provide member function implementation in Policy class."""

    def __init__(
        self: 'CalcMrcaUncertaintyExact',
        policy_spec: typing.Optional[PolicySpec],
    ) -> None:
        pass

    def __eq__(
        self: 'CalcMrcaUncertaintyExact',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, CalcMrcaUncertaintyExact)

    def __call__(
        self: 'CalcMrcaUncertaintyExact',
        policy: typing.Optional['Policy'],
        first_num_strata_deposited: int,
        second_num_strata_deposited: int,
        actual_rank_of_mrca: int,
    ) -> int:
        """Exactly how much uncertainty to estimate rank of MRCA?"""

        spec = policy.GetSpec()

        least_num_strata_deposited = min(
            first_num_strata_deposited,
            second_num_strata_deposited,
        )
        least_last_rank = least_num_strata_deposited - 1
        # mrca at very last rank
        if actual_rank_of_mrca == least_last_rank:
            return 0
        # haven't added enough ranks to hit resolution
        elif least_last_rank < spec._fixed_resolution:
            return least_last_rank - 1
        # mrca between last regularly-spaced rank and tail rank
        elif actual_rank_of_mrca >= (
            least_last_rank - least_last_rank % spec._fixed_resolution
        ):
            return (least_last_rank - 1) % spec._fixed_resolution
        # mrca between two regularly-spaced ranks
        else:
            return spec._fixed_resolution - 1
