import itertools as it
import numpy as np
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
@pytest.mark.parametrize(
    'time_sequence',
    [
        it.chain(
            range(10**3),
            np.logspace(10, 32, num=10**3, base=2, dtype='int'),
        ),
        (i for i in range(10**2) for __ in range(2)),
        np.random.default_rng(1).integers(
            low=0,
            high=2**32,
            size=10**2,
        ),
    ],
)
def test_policy_consistency(recency_proportional_resolution, time_sequence):
    policy = recency_proportional_resolution_policy.Policy(recency_proportional_resolution)
    spec = policy.GetSpec()
    instance = recency_proportional_resolution_policy.CalcMrcaUncertaintyRelExact(spec)
    for num_strata_deposited in time_sequence:
        retained_ranks = np.fromiter(
            policy.IterRetainedRanks(num_strata_deposited),
            int,
        )
        for actual_mrca_rank in it.chain(
            range(min(num_strata_deposited, 10**3)),
            np.random.default_rng(1).integers(
                low=0,
                high=num_strata_deposited,
                size=10**2,
            ) if num_strata_deposited else iter(()),
        ):
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
            recency = max(
                num_strata_deposited - 1 - actual_mrca_rank,
                1,
            )
            policy_requirement = (
                first_known_disparity - last_known_commonality - 1
            ) / recency
            assert policy_requirement >= 0
            for which in (
                instance,
                recency_proportional_resolution_policy.CalcMrcaUncertaintyRelExact(spec),
            ):
                assert which(
                    policy,
                    num_strata_deposited,
                    num_strata_deposited,
                    actual_mrca_rank,
                ) == policy_requirement

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
def test_policy_consistency_uneven_branches(recency_proportional_resolution):
    policy = recency_proportional_resolution_policy.Policy(recency_proportional_resolution)
    spec = policy.GetSpec()
    instance = recency_proportional_resolution_policy.CalcMrcaUncertaintyRelExact(spec)
    sample_durations = it.chain(
        range(10**2),
        np.logspace(7, 16, num=10, base=2, dtype='int'),
    )
    for num_strata_deposited_a in sample_durations:
        ranks_a = set(policy.IterRetainedRanks(num_strata_deposited_a))
        for num_strata_deposited_b in sample_durations:
            ranks_b = set(policy.IterRetainedRanks(num_strata_deposited_b))
            retained_ranks = np.fromiter(ranks_a & ranks_b, int)
            least_num_strata_deposited = min(
                num_strata_deposited_a,
                num_strata_deposited_b,
            )
            for actual_mrca_rank in range(least_num_strata_deposited):
                last_known_commonality = retained_ranks[
                    retained_ranks <= actual_mrca_rank,
                ].max(
                    initial=0,
                )
                first_known_disparity = retained_ranks[
                    retained_ranks > actual_mrca_rank,
                ].min(
                    initial=least_num_strata_deposited,
                )
                recency = max(
                    least_num_strata_deposited - 1 - actual_mrca_rank,
                    1,
                )
                policy_requirement = (
                    first_known_disparity - last_known_commonality - 1
                ) / recency
                assert policy_requirement >= 0
                for which in (
                    instance,
                    recency_proportional_resolution_policy.CalcMrcaUncertaintyRelExact(spec),
                ):
                    assert which(
                        policy,
                        num_strata_deposited_a,
                        num_strata_deposited_b,
                        actual_mrca_rank,
                    ) == policy_requirement

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
    spec = policy.GetSpec()
    instance = recency_proportional_resolution_policy.CalcMrcaUncertaintyRelExact(spec)

    assert instance == instance
    assert instance == recency_proportional_resolution_policy.CalcMrcaUncertaintyRelExact(spec)
    assert not instance == None
