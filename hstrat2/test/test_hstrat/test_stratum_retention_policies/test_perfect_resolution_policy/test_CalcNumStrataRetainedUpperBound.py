import numpy as np
import pytest

from hstrat2.hstrat import perfect_resolution_policy


@pytest.mark.parametrize(
    "time_sequence",
    [
        range(10**2),
        (i for i in range(10**2) for __ in range(2)),
        np.random.default_rng(1).integers(
            low=0,
            high=2**32,
            size=10**2,
        ),
    ],
)
def test_policy_consistency(time_sequence):
    policy = perfect_resolution_policy.Policy()
    spec = policy.GetSpec()
    instance = perfect_resolution_policy.CalcNumStrataRetainedUpperBound(spec)
    for num_strata_deposited in time_sequence:
        policy_requirement = policy.CalcNumStrataRetainedExact(
            num_strata_deposited,
        )
        for which in (
            instance,
            perfect_resolution_policy.CalcNumStrataRetainedUpperBound(spec),
        ):
            assert (
                which(
                    policy,
                    num_strata_deposited,
                )
                >= policy_requirement
            )


def test_eq():
    policy = perfect_resolution_policy.Policy()
    spec = policy.GetSpec()
    instance = perfect_resolution_policy.CalcNumStrataRetainedUpperBound(spec)

    assert instance == instance
    assert (
        instance
        == perfect_resolution_policy.CalcNumStrataRetainedUpperBound(
            spec,
        )
    )
    assert not instance == None
