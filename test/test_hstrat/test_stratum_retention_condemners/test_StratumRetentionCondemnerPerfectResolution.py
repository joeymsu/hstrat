from copy import deepcopy
import unittest

from pylib import hstrat


class TestStratumRetentionCondemnerPerfectResolution(unittest.TestCase):

    # tests can run independently
    _multiprocess_can_split_ = True

    def test_equality(self):
        assert (
            hstrat.StratumRetentionCondemnerPerfectResolution()
            == hstrat.StratumRetentionCondemnerPerfectResolution()
        )

        original = hstrat.StratumRetentionCondemnerPerfectResolution()
        copy = deepcopy(original)
        assert original == copy

    def test_condemnation(self):
        maximal_retention_condemner \
            = hstrat.StratumRetentionCondemnerPerfectResolution()
        for i in range(100):
            assert list(maximal_retention_condemner(
                retained_ranks=range(i),
                num_stratum_depositions_completed=i,
            )) == []

    def test_retention(self):
        control_column = hstrat.HereditaryStratigraphicColumn(
            stratum_ordered_store_factory
                =hstrat.HereditaryStratumOrderedStoreDict,
            stratum_retention_predicate
                =hstrat.StratumRetentionPredicatePerfectResolution(),
        )
        test_column = hstrat.HereditaryStratigraphicColumn(
            stratum_ordered_store_factory
                =hstrat.HereditaryStratumOrderedStoreDict,
            stratum_retention_condemner
                =hstrat.StratumRetentionCondemnerPerfectResolution(),
        )

        for i in range(1000):
            control_column.DepositStratum()
            test_column.DepositStratum()
            d1, d2 = control_column.DiffRetainedRanks(test_column)
            assert d1 == set() and d2 == set()

    def test_CalcRankAtColumnIndex(self):
        test_condemner = hstrat.StratumRetentionCondemnerPerfectResolution()
        test_column = hstrat.HereditaryStratigraphicColumn(
            always_store_rank_in_stratum=True,
            stratum_ordered_store_factory
                =hstrat.HereditaryStratumOrderedStoreDict,
            stratum_retention_condemner=test_condemner,
        )

        for i in range(1000):
            test_column.DepositStratum()
            actual_ranks = { *test_column.GetRetainedRanks() }
            calcualted_ranks = {
                test_condemner.CalcRankAtColumnIndex(
                    index=i,
                    num_strata_deposited=test_column.GetNumStrataDeposited()
                )
                for i in range(test_column.GetNumStrataRetained())
            }
            assert actual_ranks == calcualted_ranks
            # in-progress deposition case
            assert test_condemner.CalcRankAtColumnIndex(
                index=test_column.GetNumStrataRetained(),
                num_strata_deposited=test_column.GetNumStrataDeposited(),
            ) == test_column.GetNumStrataDeposited()


if __name__ == '__main__':
    unittest.main()
