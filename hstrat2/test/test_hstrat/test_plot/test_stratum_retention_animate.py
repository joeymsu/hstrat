import pytest
import unittest

from hstrat2 import hstrat


@pytest.mark.parametrize(
    'policy',
    [
        hstrat.geom_seq_nth_root_policy.Policy(4),
    ],
)
def test_one(policy):
    res = hstrat.stratum_retention_animate(
        policy,
        10,
        draw_extant_history=False,
        draw_extinct_history=False,
        draw_extinct_placeholders=True,
    )
    res = hstrat.stratum_retention_animate(
        policy,
        10,
        draw_extant_history=True,
        draw_extinct_history=False,
        draw_extinct_placeholders=True,
    )
    res = hstrat.stratum_retention_animate(
        policy,
        10,
    )

@pytest.mark.parametrize(
    'policy',
    [
        policy_t(
            parameterizer=hstrat.PropertyExactlyParameterizer(
                target_value=target_value,
                policy_evaluator \
                    =hstrat.MrcaUncertaintyAbsExactPolicyEvaluator(
                        at_num_strata_deposited=256,
                        at_rank=0,
                ),
                param_lower_bound=lb,
                param_upper_bound=1024,
            )
        )
        for policy_t, lb in (
            (hstrat.fixed_resolution_policy.Policy, 1),
            (hstrat.depth_proportional_resolution_policy.Policy, 1),
            (hstrat.depth_proportional_resolution_tapered_policy.Policy, 1),
            (hstrat.recency_proportional_resolution_policy.Policy, 0),
        )
        for target_value in (31, 127)
    ] + [
        policy_t(
            parameterizer=hstrat.PropertyAtLeastParameterizer(
                target_value=31,
                policy_evaluator \
                    =hstrat.MrcaUncertaintyAbsExactPolicyEvaluator(
                        at_num_strata_deposited=256,
                        at_rank=0,
                ),
                param_lower_bound=1,
                param_upper_bound=1024,
            )
        )
        for policy_t in (
            hstrat.geom_seq_nth_root_policy.Policy,
            hstrat.geom_seq_nth_root_tapered_policy.Policy,
        )
    ] + [
        hstrat.geom_seq_nth_root_policy.Policy(
            parameterizer=hstrat.PropertyExactlyParameterizer(
                target_value=127,
                policy_evaluator \
                    =hstrat.MrcaUncertaintyAbsExactPolicyEvaluator(
                        at_num_strata_deposited=256,
                        at_rank=0,
                ),
                param_lower_bound=1,
                param_upper_bound=1024,
            )
        )
    ] + [
        hstrat.geom_seq_nth_root_tapered_policy.Policy(
            parameterizer=hstrat.PropertyAtMostParameterizer(
                target_value=127,
                policy_evaluator \
                    =hstrat.MrcaUncertaintyAbsExactPolicyEvaluator(
                        at_num_strata_deposited=256,
                        at_rank=0,
                ),
                param_lower_bound=1,
                param_upper_bound=1024,
            )
        )
    ]
)
def test_doc_animations(policy):
    res = hstrat.stratum_retention_animate(
        policy,
        256,
        save_as='gif',
    )

@pytest.mark.parametrize(
    'policy',
    [
        hstrat.depth_proportional_resolution_tapered_policy.Policy(
            parameterizer=hstrat.PropertyAtMostParameterizer(
                target_value=10,
                policy_evaluator \
                    =hstrat.NumStrataRetainedExactPolicyEvaluator(
                        at_num_strata_deposited=256,
                ),
                param_lower_bound=1,
                param_upper_bound=1024,
            )
        )
    ]
)
def test_more_doc_animations(policy):

    res = hstrat.stratum_retention_animate(
        policy,
        10,
        draw_extant_history=False,
        draw_extinct_history=False,
        draw_extinct_placeholders=True,
        save_as='gif',
    )
    res = hstrat.stratum_retention_animate(
        policy,
        10,
        draw_extant_history=True,
        draw_extinct_history=False,
        draw_extinct_placeholders=True,
        save_as='gif',
    )
    res = hstrat.stratum_retention_animate(
        policy,
        10,
        save_as='gif',
    )
