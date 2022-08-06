import itertools as it
import numpy as np
import pytest

from hstrat2.helpers import all_same
from hstrat2.hstrat import fixed_resolution_policy


@pytest.mark.parametrize(
    'fixed_resolution',
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
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
def test_impl_consistency(fixed_resolution, time_sequence):
    policy = fixed_resolution_policy.Policy(fixed_resolution)
    spec = policy.GetSpec()
    impls = [
        *fixed_resolution_policy._GenDropRanks.iter_impls()
    ]
    instances = [
        impl(spec)
        for impl in impls
    ]
    for num_strata_deposited in time_sequence:
        assert all_same(it.chain(
            (
                sorted(impl(spec)(
                    policy,
                    num_strata_deposited,
                    policy.IterRetainedRanks(num_strata_deposited),
                ))
                for impl in impls
            ),
            (
                sorted(instance(
                    policy,
                    num_strata_deposited,
                    policy.IterRetainedRanks(num_strata_deposited),
                ))
                for instance in instances
            )
        ))

@pytest.mark.parametrize(
    'fixed_resolution',
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
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
def test_policy_consistency(fixed_resolution, time_sequence):
    policy = fixed_resolution_policy.Policy(fixed_resolution)
    spec = policy.GetSpec()
    instance = fixed_resolution_policy.GenDropRanks(spec)
    for num_strata_deposited in time_sequence:
        policy_requirement = {*policy.IterRetainedRanks(
            num_strata_deposited,
        )} - {*policy.IterRetainedRanks(
            num_strata_deposited + 1,
        )}
        for which in (
            instance,
            fixed_resolution_policy.GenDropRanks(spec),
        ):
            assert sorted(which(
                policy,
                num_strata_deposited,
                policy.IterRetainedRanks(num_strata_deposited)
            )) == sorted(policy_requirement)

@pytest.mark.parametrize(
    'fixed_resolution',
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
def test_eq(fixed_resolution):
    policy = fixed_resolution_policy.Policy(fixed_resolution)
    spec = policy.GetSpec()
    instance = fixed_resolution_policy.GenDropRanks(spec)

    assert instance == instance
    assert instance == fixed_resolution_policy.GenDropRanks(spec)
    assert not instance == None
