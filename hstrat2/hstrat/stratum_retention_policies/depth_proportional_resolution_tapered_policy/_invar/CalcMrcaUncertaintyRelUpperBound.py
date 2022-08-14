import typing

from ..PolicySpec import PolicySpec


class CalcMrcaUncertaintyRelUpperBound:
    """Functor to provide member function implementation in Policy class."""

    def __init__(
        self: 'CalcMrcaUncertaintyRelUpperBound',
        policy_spec: typing.Optional[PolicySpec],
    ) -> None:
        pass

    def __eq__(
        self: 'CalcMrcaUncertaintyRelUpperBound',
        other: typing.Any,
    ) -> bool:
        return isinstance(other, self.__class__)

    def __call__(
        self: 'CalcMrcaUncertaintyRelUpperBound',
        policy: 'Policy',
        first_num_strata_deposited: int,
        second_num_strata_deposited: int,
        actual_rank_of_mrca: int,
    ) -> float:
        """At most, how much relative uncertainty to estimate rank of MRCA? Inclusive."""

        spec = policy.GetSpec()

        if (
            first_num_strata_deposited <= 2
            or second_num_strata_deposited <= 2
            or actual_rank_of_mrca in (
                first_num_strata_deposited - 1,
                second_num_strata_deposited - 1,
            )
        ):
            return 0.0

        abs_upper_bound = policy.CalcMrcaUncertaintyAbsUpperBound(
            first_num_strata_deposited,
            second_num_strata_deposited,
            actual_rank_of_mrca,
        )

        least_last_rank = min(
            first_num_strata_deposited - 1,
            second_num_strata_deposited - 1,
        )
        least_recency = (
            least_last_rank - actual_rank_of_mrca
            if actual_rank_of_mrca is not None
            else 1
        )

        return abs_upper_bound / least_recency
