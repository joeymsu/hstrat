import typing

import numpy as np

from ..._auxiliary_lib import iter_monotonic_equivalencies, jit
from ...frozen_instrumentation import HereditaryStratigraphicSpecimen


@jit(nopython=True)
def _compare_differentia_at_common_ranks(
    first_ranks: np.array,
    first_differentiae: np.array,
    second_ranks: np.array,
    second_differentiae: np.array,
) -> typing.Tuple[int, bool]:
    for pos1, pos2 in iter_monotonic_equivalencies(first_ranks, second_ranks):
        assert first_ranks[pos1] == second_ranks[pos2]
        yield (
            first_ranks[pos1],
            first_differentiae[pos1] == second_differentiae[pos2],
        )


def iter_mutual_ranks(
    first: HereditaryStratigraphicSpecimen,
    second: HereditaryStratigraphicSpecimen,
    compare: bool = False,
) -> typing.Union[
    typing.Iterator[int],
    typing.Iterator[typing.Tuple[int, bool]],
]:
    """Iterate over ranks with matching strata between columns in ascending
    order."""
    if compare:
        return _compare_differentia_at_common_ranks(
            first.GetRankIndex(),
            first.GetDifferentiaVals(),
            second.GetRankIndex(),
            second.GetDifferentiaVals(),
        )

    else:
        assert all(
            first.GetRankIndex()[first_idx] == second.GetRankIndex()[second]
            and isinstance(first.GetRankIndex()[first_idx], np.integer)
            for first_idx, second_idx in iter_monotonic_equivalencies(
                first.GetRankIndex(), second.GetRankIndex()
            )
        )
        return (
            # convert to Python int because elsewhere
            # numpy ints are experiencing unwanted conversion to floats
            int(first.GetRankIndex()[first_idx])
            for first_idx, _second_idx in iter_monotonic_equivalencies(
                first.GetRankIndex(), second.GetRankIndex()
            )
        )
