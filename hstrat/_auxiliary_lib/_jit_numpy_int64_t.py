"""Provides numba int64 type or numpy int64 type.

Type must be declared outside jit'ed function or numba fails.
"""

import numpy as np

from ._is_in_coverage_run import is_in_coverage_run

try:
    import numba as nb
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    jit_numpy_int64_t = np.int64
else:
    if is_in_coverage_run():
        # when numba disabled for coverage testing,
        # using nb.types.int64_ causes numpy TypeError
        jit_numpy_int64_t = np.int64
    else:  # pragma: no cover
        # exclude from coverage because jit compilation disabled in cov runs
        jit_numpy_int64_t = nb.types.int64
