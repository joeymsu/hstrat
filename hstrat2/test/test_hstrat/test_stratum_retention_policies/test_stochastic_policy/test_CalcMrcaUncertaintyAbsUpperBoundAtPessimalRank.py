import random

import numpy as np
import pytest

from hstrat2.hstrat import stochastic_policy
from hstrat2.hstrat.stratum_retention_policies._detail import (
    CalcMrcaUncertaintyAbsUpperBoundPessimalRankBruteForce,
)


@pytest.mark.parametrize(
    'replicate',
    range(5),
)
@pytest.mark.parametrize(
    'time_sequence',
    [
        range(10**2),
        np.random.default_rng(1).integers(
            10**3,
            size=10**2,
        )
    ],
)
def test_policy_consistency(replicate, time_sequence):
    random.seed(replicate)
    policy = stochastic_policy.Policy()
    spec = policy.GetSpec()
    instance = stochastic_policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank(
        spec,
    )
    for num_strata_deposited_a in time_sequence:
        for num_strata_deposited_b in (
            num_strata_deposited_a // 3,
            num_strata_deposited_a // 2,
            num_strata_deposited_a,
            num_strata_deposited_a + 1,
            num_strata_deposited_a + 10,
            num_strata_deposited_a + 100,
        ):
            if 0 in (num_strata_deposited_a, num_strata_deposited_b):
                continue
            for actual_mrca_rank in np.random.default_rng(1).integers(
                min(num_strata_deposited_a, num_strata_deposited_b),
                size=3,
            ):
                policy_requirement = policy.CalcMrcaUncertaintyAbsUpperBound(
                    num_strata_deposited_a,
                    num_strata_deposited_b,
                    CalcMrcaUncertaintyAbsUpperBoundPessimalRankBruteForce()(
                        policy,
                        num_strata_deposited_a,
                        num_strata_deposited_b,
                    ),
                )
                for which in (
                    instance,
                    stochastic_policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank(spec)
                ):
                    assert which(
                        policy,
                        num_strata_deposited_a,
                        num_strata_deposited_b,
                    ) == policy_requirement

@pytest.mark.parametrize(
    'replicate',
    range(5),
)
def test_eq(replicate):
    random.seed(replicate)
    policy = stochastic_policy.Policy()
    spec = policy.GetSpec()
    instance = stochastic_policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank(
        spec,
    )
    instance = stochastic_policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank(spec)

    assert instance == instance
    assert instance == stochastic_policy.CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank(
        spec,
    )
    assert not instance == None
