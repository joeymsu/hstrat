#pragma once
#ifndef HSTRAT_STRATUM_RETENTION_STRATEGY_STRATUM_RETENTION_ALGORITHMS_FIXED_RESOLUTION_ALGO_INVAR_CALCMRCAUNCERTAINTYABSUPPERBOUNDATPESSIMALRANKFTOR_HPP_INCLUDE
#define HSTRAT_STRATUM_RETENTION_STRATEGY_STRATUM_RETENTION_ALGORITHMS_FIXED_RESOLUTION_ALGO_INVAR_CALCMRCAUNCERTAINTYABSUPPERBOUNDATPESSIMALRANKFTOR_HPP_INCLUDE

namespace hstrat {
namespace fixed_resolution_algo {

struct CalcMrcaUncertaintyAbsUpperBoundAtPessimalRankFtor {

  template<typename POLICY_SPEC>
  explicit CalcMrcaUncertaintyAbsUpperBoundAtPessimalRankFtor(
    const POLICY_SPEC&
  ) {}

  template<typename POLICY>
  void operator()(const POLICY& policy) const {

  }

};

} // namespace fixed_resolution_algo
} // namespace hstrat

#endif // #ifndef HSTRAT_STRATUM_RETENTION_STRATEGY_STRATUM_RETENTION_ALGORITHMS_FIXED_RESOLUTION_ALGO_INVAR_CALCMRCAUNCERTAINTYABSUPPERBOUNDATPESSIMALRANKFTOR_HPP_INCLUDE
