#pragma once
#ifndef HSTRAT_AUXLIB_SAFE_CAST_HPP_INCLUDE
#define HSTRAT_AUXLIB_SAFE_CAST_HPP_INCLUDE

#include <limits>
#include <stddef.h>
#include <stdexcept>
#include <string>

#include "safe_compare.hpp"

// copied from https://github.com/mmore500/conduit/blob/master/include/uitsl/debug/
namespace hstrat_auxlib {

// adapted from https://stackoverflow.com/a/49658950
template<typename Dst, typename Src>
inline Dst safe_cast(const Src value)
{
  typedef std::numeric_limits<Dst> DstLim;
  typedef std::numeric_limits<Src> SrcLim;

  const bool positive_overflow_possible = safe_less(
    DstLim::max(),
    SrcLim::max()
  );
  const bool negative_overflow_possible =
      SrcLim::is_signed
      or
      safe_greater(DstLim::lowest(), SrcLim::lowest());

  // unsigned <-- unsigned
  if((not DstLim::is_signed) and (not SrcLim::is_signed)) {
    if(positive_overflow_possible and (value > DstLim::max())) {
      throw std::overflow_error(__PRETTY_FUNCTION__ +
                    std::string(": positive overflow"));
    }
  }
  // unsigned <-- signed
  else if((not DstLim::is_signed) and SrcLim::is_signed) {
    if(positive_overflow_possible and safe_greater(value, DstLim::max())) {
      throw std::overflow_error(__PRETTY_FUNCTION__ +
                    std::string(": positive overflow"));
    }
    else if(negative_overflow_possible and (value < 0)) {
      throw std::overflow_error(__PRETTY_FUNCTION__ +
                    std::string(": negative overflow"));
    }

  }
  // signed <-- unsigned
  else if(DstLim::is_signed and (not SrcLim::is_signed)) {
    if(positive_overflow_possible and safe_greater(value, DstLim::max())) {
      throw std::overflow_error(__PRETTY_FUNCTION__ +
                    std::string(": positive overflow"));
    }
  }
  // signed <-- signed
  else if(DstLim::is_signed and SrcLim::is_signed) {
    if(positive_overflow_possible and safe_greater(value, DstLim::max())) {
      throw std::overflow_error(__PRETTY_FUNCTION__ +
                    std::string(": positive overflow"));
    } else if(negative_overflow_possible and safe_less(value, DstLim::lowest())) {
      throw std::overflow_error(__PRETTY_FUNCTION__ +
                    std::string(": negative overflow"));
    }
  }

  // limits have been checked, therefore safe to cast
  return static_cast<Dst>(value);
}

// copied from https://github.com/mmore500/conduit/blob/master/include/uitsl/debug/
} // namespace hstrat_auxlib

#endif // #ifndef HSTRAT_AUXLIB_SAFE_CAST_HPP_INCLUDE
