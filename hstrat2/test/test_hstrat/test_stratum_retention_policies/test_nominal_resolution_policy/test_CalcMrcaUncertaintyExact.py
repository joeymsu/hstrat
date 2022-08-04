import numpy as np
import pytest

from hstrat2.hstrat import nominal_resolution_policy


@pytest.mark.parametrize(
    'time_sequence',
    [
        range(10**2),
        (i for i in range(10**2) for __ in range(2)),
        np.random.default_rng(1).integers(
            low=0,
            high=10**3,
            size=10**2,
        ),
    ],
)
def test_policy_consistency(time_sequence):
    policy = nominal_resolution_policy.Policy()
    spec = policy.GetSpec()
    instance = nominal_resolution_policy.CalcMrcaUncertaintyExact(spec)
    for num_strata_deposited in time_sequence:
        for actual_mrca_rank in range(num_strata_deposited):
            retained_ranks = np.fromiter(
                policy.IterRetainedRanks(num_strata_deposited),
                int,
            )
            last_known_commonality = retained_ranks[
                retained_ranks <= actual_mrca_rank,
            ].max(
                initial=0,
            )
            first_known_disparity = retained_ranks[
                retained_ranks > actual_mrca_rank,
            ].min(
                initial=num_strata_deposited,
            )
            policy_requirement \
                =  first_known_disparity - last_known_commonality - 1
            assert policy_requirement >= 0
            for which in (
                instance,
                nominal_resolution_policy.CalcMrcaUncertaintyExact(spec),
            ):
                assert which(
                    policy,
                    num_strata_deposited,
                    num_strata_deposited,
                    actual_mrca_rank,
                ) == policy_requirement

def test_eq():
    policy = nominal_resolution_policy.Policy()
    spec = policy.GetSpec()
    instance = nominal_resolution_policy.CalcMrcaUncertaintyExact(spec)

    assert instance == instance
    assert instance == nominal_resolution_policy.CalcMrcaUncertaintyExact(spec)
    assert not instance == None
