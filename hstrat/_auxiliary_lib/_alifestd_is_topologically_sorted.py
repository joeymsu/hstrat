import numpy as np
import pandas as pd

from ._alifestd_has_compact_ids import alifestd_has_compact_ids
from ._alifestd_has_contiguous_ids import alifestd_has_contiguous_ids
from ._alifestd_parse_ancestor_ids import alifestd_parse_ancestor_ids
from ._jit import jit
from ._jit_numpy_bool_t import jit_numpy_bool_t


@jit(nopython=True)
def _is_topologically_sorted_contiguous(ancestor_ids: np.array) -> bool:
    for id, ancestor_id in enumerate(ancestor_ids):
        if id < ancestor_id:
            return False
    return True


@jit(nopython=True)
def _is_topologically_sorted_compact(
    ids: np.array, ancestor_ids: np.array
) -> bool:
    seen_ancestor_ids = np.zeros(len(ids), dtype=jit_numpy_bool_t)
    for id, ancestor_id in zip(ids, ancestor_ids):
        if seen_ancestor_ids[id]:
            return False
        seen_ancestor_ids[ancestor_id] = True
    return True


@jit(nopython=True)
def _is_topologically_sorted(ids: np.array, ancestor_ids: np.array) -> bool:
    seen_ancestor_ids = set()
    for id, ancestor_id in zip(ids, ancestor_ids):
        if id in seen_ancestor_ids:
            return False
        seen_ancestor_ids.add(ancestor_id)
    return True


def alifestd_is_topologically_sorted(phylogeny_df: pd.DataFrame) -> bool:
    """Are all organisms listed after members of their `ancestor_list`?"""

    if "ancestor_id" in phylogeny_df:
        if alifestd_has_contiguous_ids(phylogeny_df):
            return _is_topologically_sorted_contiguous(
                phylogeny_df["ancestor_id"].to_numpy()
            )
        elif alifestd_has_compact_ids(phylogeny_df):
            return _is_topologically_sorted_compact(
                phylogeny_df["id"].to_numpy(),
                phylogeny_df["ancestor_id"].to_numpy(),
            )
        else:
            return _is_topologically_sorted(
                phylogeny_df["id"].to_numpy(),
                phylogeny_df["ancestor_id"].to_numpy(),
            )

    phylogeny_df = phylogeny_df.set_index("id", drop=False)

    for pos, (_idx, row) in enumerate(phylogeny_df.iterrows()):
        for ancestor_id in alifestd_parse_ancestor_ids(row["ancestor_list"]):
            if phylogeny_df.index.get_loc(ancestor_id) >= pos:
                return False

    return True
