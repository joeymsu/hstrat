from hstrat2.hstrat import nominal_resolution_policy


def test_init():
    assert (
        nominal_resolution_policy.Policy().GetSpec()
        == nominal_resolution_policy.Policy(
            policy_spec=nominal_resolution_policy.PolicySpec(),
        ).GetSpec()
    )

    policy = nominal_resolution_policy.Policy()

    # invariants
    assert callable(policy.CalcMrcaUncertaintyAbsUpperBound)
    assert callable(policy.CalcNumStrataRetainedUpperBound)
    # scrying
    assert callable(policy.CalcMrcaUncertaintyAbsExact)
    assert callable(policy.CalcMrcaUncertaintyRelExact)
    assert callable(policy.CalcNumStrataRetainedExact)
    assert callable(policy.CalcRankAtColumnIndex)
    assert callable(policy.IterRetainedRanks)
    # enactment
    assert callable(policy.GenDropRanks)


def test_eq():
    policy = nominal_resolution_policy.Policy()
    assert policy == policy
    assert policy == nominal_resolution_policy.Policy()
    assert policy != policy.WithoutCalcRankAtColumnIndex()
    assert policy.WithoutCalcRankAtColumnIndex() \
        == policy.WithoutCalcRankAtColumnIndex()

def test_GetSpec():
    assert nominal_resolution_policy.Policy().GetSpec()

def test_WithoutCalcRankAtColumnIndex():

    original = nominal_resolution_policy.Policy()
    stripped = original.WithoutCalcRankAtColumnIndex()

    assert stripped.CalcRankAtColumnIndex is None

    assert original.CalcMrcaUncertaintyAbsUpperBound \
        == stripped.CalcMrcaUncertaintyAbsUpperBound
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
    assert nominal_resolution_policy.Policy().WithoutCalcRankAtColumnIndex() \
        == stripped

def test_repr():
    policy = nominal_resolution_policy.Policy()
    assert policy.GetSpec().GetPolicyName() in repr(policy)

def test_str():
    policy = nominal_resolution_policy.Policy()
    assert policy.GetSpec().GetPolicyTitle() in str(policy)
