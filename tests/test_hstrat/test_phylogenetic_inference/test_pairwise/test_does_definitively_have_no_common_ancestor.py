import pytest

from hstrat import hstrat


@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.nominal_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
        hstrat.recency_proportional_resolution_algo.Policy(
            recency_proportional_resolution=2
        ),
    ],
)
@pytest.mark.parametrize(
    "differentia_width",
    [1, 2, 8, 64],
)
def test_does_definitively_have_no_common_ancestor_specimen(
    retention_policy, differentia_width
):
    column = hstrat.HereditaryStratigraphicColumn(
        stratum_retention_policy=retention_policy,
        stratum_differentia_bit_width=differentia_width,
    )
    for generation in range(100):
        column.DepositStratum()

    child1 = column.CloneDescendant()
    child2 = column.CloneDescendant()

    assert hstrat.does_definitively_have_no_common_ancestor(
        hstrat.col_to_specimen(column), hstrat.col_to_specimen(column)
    ) == hstrat.does_definitively_have_no_common_ancestor(column, column)

    assert hstrat.does_definitively_have_no_common_ancestor(
        hstrat.col_to_specimen(column), hstrat.col_to_specimen(child1)
    ) == hstrat.does_definitively_have_no_common_ancestor(column, child1)

    assert hstrat.does_definitively_have_no_common_ancestor(
        hstrat.col_to_specimen(child1), hstrat.col_to_specimen(child2)
    ) == hstrat.does_definitively_have_no_common_ancestor(child1, child2)

    child1.DepositStrata(10)
    assert hstrat.does_definitively_have_no_common_ancestor(
        hstrat.col_to_specimen(child1), hstrat.col_to_specimen(child2)
    ) == hstrat.does_definitively_have_no_common_ancestor(child1, child2)


@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
        hstrat.recency_proportional_resolution_algo.Policy(
            recency_proportional_resolution=10,
        ),
    ],
)
def test_DefinitivelySharesNoCommonAncestorWith1(retention_policy):
    while True:
        c1 = hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=1,
            stratum_retention_policy=retention_policy,
        )
        c2 = hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=1,
            stratum_retention_policy=retention_policy,
        )
        if hstrat.does_definitively_have_no_common_ancestor(c1, c2):
            assert hstrat.does_definitively_have_no_common_ancestor(c2, c1)
            for __ in range(100):
                c1.DepositStratum()
                assert hstrat.does_definitively_have_no_common_ancestor(c1, c2)
                assert hstrat.does_definitively_have_no_common_ancestor(c2, c1)
            for __ in range(100):
                c2.DepositStratum()
                assert hstrat.does_definitively_have_no_common_ancestor(c1, c2)
                assert hstrat.does_definitively_have_no_common_ancestor(c2, c1)
            break

    while True:
        c1 = hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=1,
            stratum_retention_policy=retention_policy,
        )
        c2 = hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=1,
            stratum_retention_policy=retention_policy,
        )
        if not hstrat.does_definitively_have_no_common_ancestor(c1, c2):
            assert not hstrat.does_definitively_have_no_common_ancestor(c2, c1)
            for __ in range(100):
                c1.DepositStratum()
                assert not hstrat.does_definitively_have_no_common_ancestor(
                    c1, c2
                )
                assert not hstrat.does_definitively_have_no_common_ancestor(
                    c2, c1
                )
            for __ in range(100):
                c2.DepositStratum()
                assert not hstrat.does_definitively_have_no_common_ancestor(
                    c1, c2
                )
                assert not hstrat.does_definitively_have_no_common_ancestor(
                    c2, c1
                )
            break

    for rep in range(100):
        c1 = hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=64,
            stratum_retention_policy=retention_policy,
        )
        c2 = hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=64,
            stratum_retention_policy=retention_policy,
        )
        assert hstrat.does_definitively_have_no_common_ancestor(c1, c2)
        assert hstrat.does_definitively_have_no_common_ancestor(c2, c1)


@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
        hstrat.recency_proportional_resolution_algo.Policy(
            recency_proportional_resolution=10,
        ),
    ],
)
def test_DefinitivelySharesNoCommonAncestorWith2(retention_policy):

    c1 = hstrat.HereditaryStratigraphicColumn(
        stratum_differentia_bit_width=1,
        stratum_retention_policy=retention_policy,
    )
    c2 = c1.Clone()
    assert not hstrat.does_definitively_have_no_common_ancestor(c1, c2)
    assert not hstrat.does_definitively_have_no_common_ancestor(c2, c1)
    for __ in range(100):
        c1.DepositStratum()
        assert not hstrat.does_definitively_have_no_common_ancestor(c1, c2)
        assert not hstrat.does_definitively_have_no_common_ancestor(c2, c1)
    for __ in range(100):
        c2.DepositStratum()
        assert not hstrat.does_definitively_have_no_common_ancestor(c1, c2)
        assert not hstrat.does_definitively_have_no_common_ancestor(c2, c1)

    for rep in range(100):
        c1 = hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=64,
            stratum_retention_policy=retention_policy,
        )
        c2 = c1.Clone()
        assert not hstrat.does_definitively_have_no_common_ancestor(c1, c2)
        assert not hstrat.does_definitively_have_no_common_ancestor(c2, c1)
