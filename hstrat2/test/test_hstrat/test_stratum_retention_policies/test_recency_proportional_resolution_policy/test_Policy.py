import pytest

from hstrat2.hstrat import recency_proportional_resolution_policy


@pytest.mark.parametrize(
    'recency_proportional_resolution',
    [
        0,
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
def test_init(recency_proportional_resolution):
    assert (
        recency_proportional_resolution_policy.Policy(recency_proportional_resolution).GetSpec()
        == recency_proportional_resolution_policy.Policy(
            policy_spec=recency_proportional_resolution_policy.PolicySpec(recency_proportional_resolution),
        ).GetSpec()
    )

    policy = recency_proportional_resolution_policy.Policy(recency_proportional_resolution)

    # invariants
    assert callable(policy.CalcMrcaUncertaintyAbsUpperBound)
    assert callable(policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank)
    assert callable(policy.CalcMrcaUncertaintyAbsUpperBoundPessimalRank)
    assert callable(policy.CalcMrcaUncertaintyRelUpperBound)
    assert callable(policy.CalcMrcaUncertaintyRelUpperBoundAtPessimalRank)
    assert callable(policy.CalcMrcaUncertaintyRelUpperBoundPessimalRank)
    assert callable(policy.CalcNumStrataRetainedUpperBound)
    # scrying
    assert callable(policy.CalcMrcaUncertaintyAbsExact)
    assert callable(policy.CalcMrcaUncertaintyRelExact)
    assert callable(policy.CalcNumStrataRetainedExact)
    assert callable(policy.CalcRankAtColumnIndex)
    assert callable(policy.IterRetainedRanks)
    # enactment
    assert callable(policy.GenDropRanks)


@pytest.mark.parametrize(
    'recency_proportional_resolution',
    [
        0,
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
def test_eq(recency_proportional_resolution):
    policy = recency_proportional_resolution_policy.Policy(recency_proportional_resolution)
    assert policy == policy
    assert policy == recency_proportional_resolution_policy.Policy(recency_proportional_resolution)
    assert not policy == policy.WithoutCalcRankAtColumnIndex()
    assert policy.WithoutCalcRankAtColumnIndex() \
        == policy.WithoutCalcRankAtColumnIndex()
    assert not policy == recency_proportional_resolution_policy.Policy(recency_proportional_resolution + 1)

@pytest.mark.parametrize(
    'recency_proportional_resolution',
    [
        0,
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
def test_GetSpec(recency_proportional_resolution):
    assert recency_proportional_resolution_policy.Policy(recency_proportional_resolution).GetSpec() \
        == recency_proportional_resolution_policy.PolicySpec(recency_proportional_resolution)

@pytest.mark.parametrize(
    'recency_proportional_resolution',
    [
        0,
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
def test_WithoutCalcRankAtColumnIndex(recency_proportional_resolution):

    original = recency_proportional_resolution_policy.Policy(recency_proportional_resolution)
    stripped = original.WithoutCalcRankAtColumnIndex()

    assert stripped.CalcRankAtColumnIndex is None

    assert original.CalcMrcaUncertaintyAbsUpperBound \
        == stripped.CalcMrcaUncertaintyAbsUpperBound
    assert original.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank \
        == stripped.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank
    assert original.CalcMrcaUncertaintyAbsUpperBoundPessimalRank \
        == stripped.CalcMrcaUncertaintyAbsUpperBoundPessimalRank
    assert original.CalcMrcaUncertaintyRelUpperBound \
        == stripped.CalcMrcaUncertaintyRelUpperBound
    assert original.CalcMrcaUncertaintyRelUpperBoundAtPessimalRank \
        == stripped.CalcMrcaUncertaintyRelUpperBoundAtPessimalRank
    assert original.CalcMrcaUncertaintyRelUpperBoundPessimalRank \
        == stripped.CalcMrcaUncertaintyRelUpperBoundPessimalRank
    assert original.CalcNumStrataRetainedUpperBound \
        == stripped.CalcNumStrataRetainedUpperBound
    # scrying
    assert original.CalcMrcaUncertaintyAbsExact \
        == stripped.CalcMrcaUncertaintyAbsExact
    assert original.CalcMrcaUncertaintyRelExact \
        == stripped.CalcMrcaUncertaintyRelExact
    assert original.CalcNumStrataRetainedExact \
        == stripped.CalcNumStrataRetainedExact
    assert original.IterRetainedRanks == stripped.IterRetainedRanks
    # enactment
    assert original.GenDropRanks == stripped.GenDropRanks

    # test chaining
    assert recency_proportional_resolution_policy.Policy(
        recency_proportional_resolution,
    ).WithoutCalcRankAtColumnIndex() == stripped

def test_repr():
    recency_proportional_resolution = 1
    policy = recency_proportional_resolution_policy.Policy(recency_proportional_resolution)
    assert str(recency_proportional_resolution) in repr(policy)
    assert policy.GetSpec().GetPolicyName() in repr(policy)

def test_str():
    recency_proportional_resolution = 1
    policy = recency_proportional_resolution_policy.Policy(recency_proportional_resolution)
    assert str(recency_proportional_resolution) in str(policy)
    assert policy.GetSpec().GetPolicyTitle() in str(policy)
