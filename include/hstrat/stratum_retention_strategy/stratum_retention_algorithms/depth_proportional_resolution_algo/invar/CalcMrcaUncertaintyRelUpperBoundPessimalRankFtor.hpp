#pragma once
#ifndef HSTRAT_STRATUM_RETENTION_STRATEGY_STRATUM_RETENTION_ALGORITHMS_DEPTH_PROPORTIONAL_RESOLUTION_ALGO_INVAR_CALCMRCAUNCERTAINTYRELUPPERBOUNDPESSIMALRANKFTOR_HPP_INCLUDE
#define HSTRAT_STRATUM_RETENTION_STRATEGY_STRATUM_RETENTION_ALGORITHMS_DEPTH_PROPORTIONAL_RESOLUTION_ALGO_INVAR_CALCMRCAUNCERTAINTYRELUPPERBOUNDPESSIMALRANKFTOR_HPP_INCLUDE

namespace hstrat {
namespace depth_proportional_resolution_algo {

struct CalcMrcaUncertaintyRelUpperBoundPessimalRankFtor {

  template<typename POLICY_SPEC>
  explicit CalcMrcaUncertaintyRelUpperBoundPessimalRankFtor(
    const POLICY_SPEC&
  ) {}

  template<typename POLICY>
  void operator()(const POLICY& policy) const {

  }

};

} // namespace depth_proportional_resolution_algo
} // namespace hstrat

#endif // #ifndef HSTRAT_STRATUM_RETENTION_STRATEGY_STRATUM_RETENTION_ALGORITHMS_DEPTH_PROPORTIONAL_RESOLUTION_ALGO_INVAR_CALCMRCAUNCERTAINTYRELUPPERBOUNDPESSIMALRANKFTOR_HPP_INCLUDE
