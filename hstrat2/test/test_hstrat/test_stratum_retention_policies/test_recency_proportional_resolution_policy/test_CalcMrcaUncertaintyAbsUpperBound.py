import numpy as np
import pytest

from hstrat2.hstrat import recency_proportional_resolution_policy


@pytest.mark.parametrize(
    "recency_proportional_resolution",
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
    "time_sequence",
    [
        range(10**3),
        (i for i in range(10**2) for __ in range(2)),
        np.random.default_rng(1).integers(
            low=0,
            high=2**32,
            size=10,
        ),
        (2**32,),
    ],
)
def test_policy_consistency(recency_proportional_resolution, time_sequence):
    policy = recency_proportional_resolution_policy.Policy(
        recency_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = recency_proportional_resolution_policy.CalcMrcaUncertaintyAbsUpperBound(
        spec,
    )
    for num_strata_deposited in time_sequence:
        for actual_mrca_rank in (
            np.random.default_rng(num_strata_deposited,).integers(
                low=0,
                high=num_strata_deposited,
                size=10**2,
            )
            if num_strata_deposited
            else iter(())
        ):
            policy_requirement = policy.CalcMrcaUncertaintyAbsExact(
                num_strata_deposited,
                num_strata_deposited,
                actual_mrca_rank,
            )
            for which in (
                instance,
                recency_proportional_resolution_policy.CalcMrcaUncertaintyAbsUpperBound(
                    spec
                ),
            ):
                assert (
                    which(
                        policy,
                        num_strata_deposited,
                        num_strata_deposited,
                        actual_mrca_rank,
                    )
                    >= policy_requirement
                )


@pytest.mark.parametrize(
    "recency_proportional_resolution",
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
    policy = recency_proportional_resolution_policy.Policy(
        recency_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = recency_proportional_resolution_policy.CalcMrcaUncertaintyAbsUpperBound(
        spec
    )

    assert instance == instance
    assert (
        instance
        == recency_proportional_resolution_policy.CalcMrcaUncertaintyAbsUpperBound(
            spec,
        )
    )
    assert not instance == None


@pytest.mark.parametrize(
    "recency_proportional_resolution",
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
def test_negative_index(recency_proportional_resolution):
    policy = recency_proportional_resolution_policy.Policy(
        recency_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = recency_proportional_resolution_policy.CalcMrcaUncertaintyAbsUpperBound(
        spec
    )

    for diff in range(1, 100):
        assert instance(policy, 100, 100, -diff,) == instance(
            policy,
            100,
            100,
            99 - diff,
        )

        assert instance(policy, 101, 100, -diff,) == instance(
            policy,
            101,
            100,
            99 - diff,
        )

        assert instance(policy, 150, 100, -diff,) == instance(
            policy,
            150,
            100,
            99 - diff,
        )

        assert instance(policy, 100, 101, -diff,) == instance(
            policy,
            101,
            100,
            99 - diff,
        )

        assert instance(policy, 100, 150, -diff,) == instance(
            policy,
            150,
            100,
            99 - diff,
        )
