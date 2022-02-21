import gmpy
import math
import typing


class StratumRetentionPredicateRecencyProportionalResolution:

    _guaranteed_mrca_recency_proportional_resolution: int

    def __init__(
        self: 'StratumRetentionPredicateRecencyProportionalResolution',
        guaranteed_mrca_recency_proportional_resolution: int=10,
    ):
        self._guaranteed_mrca_recency_proportional_resolution = (
            guaranteed_mrca_recency_proportional_resolution
        )

    def __eq__(
        self: 'StratumRetentionPredicateRecencyProportionalResolution',
        other: 'StratumRetentionPredicateRecencyProportionalResolution',
    ) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __call__(
        self: 'StratumRetentionPredicateRecursiveInterspersion',
        stratum_rank: int,
        column_strata_deposited: int,
    ) -> bool:
        # Derivation of predicate implementation:
        #
        # To begin, let's consider setting up just the *first* rank of the
        # stratum after the root ancestor we will retain.
        #
        # root ancestor                                     extant individual
        # |                                                                 |
        # |                    num_strata_deposited                         |
        # | ___________________________/\_________________________________  |
        # |/                                                               \|
        # |-------------------|#############################################|
        #  \_______  ________/|\____________________  ______________________/
        #          \/         |                     \/
        #    max_uncertainty  |            worst_case_mrca_depth
        #                     |
        #                     proposed retention rank
        #
        # To provide guaranteed resolution, max_uncertainty must be leq than
        #
        #    worst_case_mrca_depth // guaranteed_resolution
        #
        # So, to find the largest permissible max_uncertainty we must solve
        #
        #    max_uncertainty = worst_case_mrca_depth // guaranteed_resolution
        #
        # By construction we have
        #
        #    worst_case_mrca_depth = num_strata_deposited - max_uncertainty
        #
        # Substituting into the above expression gives
        #
        #    max_uncertainty
        #    = (num_strata_deposited - max_uncertainty) // guaranteed_resolution
        #
        # Solving for max_uncertainty yields
        #
        #   max_uncertainty
        #   = num_strata_deposited // (guaranteed_resolution + 1)
        #
        # We now have an upper bound for the rank of the first stratum rank
        # we must retain. We can repeat this process recursively to select
        # ranks that give adequate resolution proportional to
        # worst_case_mrca_depth.
        #
        # However, we must guarantee that thes ranks are actually available for
        # us to retain (i.e., it hasn't been purged out of the column at a
        # previous time point as the column was grown by successive deposition).
        # We will do this by picking the rank that is the highest power of 2
        # less than or equal to our bound. If we repeat this procedure as we
        # recurse, we are guaranteed that this rank will have been preserved
        # across all previous timepoints.
        #
        # This is because a partial sum sequence where all elements are powers
        # of 2 and elements in the sequence are will include all multiples of
        # powers of 2 greater than or equal to the first element that are less
        # than or equal to the sum of the entire
        # sequence.
        #
        # An example is the best way to convince yourself. Thinking analogously
        # in base 10,
        #
        #    100 + 10... + 1...
        #
        # the partial sums of any sequence of this form will always include all
        # multiples of powers of 100, 1000, etc. that are less than or equal to
        # the sum of the entire sequence.
        #
        # In our application, partial sums represent retained ranks. So, all
        # ranks that are perfect powers of 2 measuring from the root ancestor
        # will have been retained after being deposited. This property
        # generalizes recursively.
        resolution = self._guaranteed_mrca_recency_proportional_resolution

        # to satisfy requirements of HereditaryStratigraphicColumn impl
        # we must always keep root ancestor and newest stratum
        if (stratum_rank in (0, column_strata_deposited)): return True
        elif column_strata_deposited <= resolution: return True

        max_uncertainty = column_strata_deposited // (resolution + 1)
        # round down to lower or equal power of 2
        provided_uncertainty_exp = (max_uncertainty // 2).bit_length()
        provided_uncertainty = 2 ** provided_uncertainty_exp

        # logically,  we could just test
        #   if stratum_rank == provided_uncertainty: return True
        # but we are guaranteed to eventually return True under the weaker
        # condition
        #   if stratum_rank % provided_uncertainty == 0
        # so as an optimization go ahead and return True now if it holds
        if stratum_rank % provided_uncertainty == 0: return True
        elif stratum_rank < provided_uncertainty: return False
        else: return self.__call__(
            stratum_rank - provided_uncertainty,
            column_strata_deposited - provided_uncertainty,
        )

    def CalcNumStrataRetainedUpperBound(
        self: 'StratumRetentionPredicateRecursiveInterspersion',
        num_strata_deposited: int,
    ) -> int:
        # With
        #   n = num_strata_deposited - 1
        #   r = resolution
        # the implementation below is mathematically equivalent to
        #   weight of binary expansion of n (i.e., #1's set in binary repr)
        #   + sum(
        #       floor( log2(n//r) )
        #       for r from 1 to r inclusive
        #   )
        #   + 1
        # after n < r causing log2(0) are accounted for.
        #
        # This expression for exact number deposited was extrapolated from
        # resolution = 0, https://oeis.org/A063787
        # resolution = 1, https://oeis.org/A056791
        # and is unit tested extensively.
        resolution = self._guaranteed_mrca_recency_proportional_resolution
        if num_strata_deposited - 1 <= resolution: return num_strata_deposited
        else: return (
            gmpy.popcount(num_strata_deposited - 1)
            + sum(
                # X.bit_length() - 1 equivalent to floor(log2(X))
                ((num_strata_deposited - 1) // r).bit_length() - 1
                for r in range(1, resolution + 1)
            )
            + 1
        )

    def CalcMrcaUncertaintyUpperBound(
        self: 'StratumRetentionPredicateRecencyProportionalResolution',
        *,
        actual_rank_of_mrca: int,
        first_num_strata_deposited: int,
        second_num_strata_deposited: int,
    ) -> int:
        max_ranks_since_mrca = max(
            first_num_strata_deposited,
            second_num_strata_deposited,
        ) - actual_rank_of_mrca
        if self._guaranteed_mrca_recency_proportional_resolution == 0:
            return min(first_num_strata_deposited, second_num_strata_deposited)
        else: return (
            max_ranks_since_mrca
            // self._guaranteed_mrca_recency_proportional_resolution
        )
