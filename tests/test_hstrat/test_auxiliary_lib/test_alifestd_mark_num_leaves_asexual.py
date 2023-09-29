import os

import pandas as pd
import pytest

from hstrat._auxiliary_lib import (
    alifestd_find_leaf_ids,
    alifestd_find_root_ids,
    alifestd_has_multiple_roots,
    alifestd_make_empty,
    alifestd_mark_num_leaves_asexual,
    alifestd_validate,
)

assets_path = os.path.join(os.path.dirname(__file__), "assets")


@pytest.mark.parametrize(
    "phylogeny_df",
    [
        pd.read_csv(
            f"{assets_path}/example-standard-toy-asexual-phylogeny.csv"
        ),
        pd.read_csv(f"{assets_path}/nk_ecoeaselection.csv"),
        pd.read_csv(f"{assets_path}/nk_lexicaseselection.csv"),
        pd.read_csv(f"{assets_path}/nk_tournamentselection.csv"),
    ],
)
def test_fuzz(phylogeny_df: pd.DataFrame):
    original = phylogeny_df.copy()

    result = alifestd_mark_num_leaves_asexual(phylogeny_df)

    assert alifestd_validate(result)
    assert original.equals(phylogeny_df)

    leaf_ids = [*alifestd_find_leaf_ids(phylogeny_df)]
    for leaf_id in leaf_ids:
        num_leaves = result[result["id"] == leaf_id]["num_leaves"].squeeze()
        assert num_leaves == 1

    assert not alifestd_has_multiple_roots(phylogeny_df)
    (root_id,) = alifestd_find_root_ids(phylogeny_df)
    num_leaves = result[result["id"] == root_id]["num_leaves"].squeeze()
    assert num_leaves == len(leaf_ids)

    assert all(1 <= result["num_leaves"])
    assert all(result["num_leaves"] <= len(leaf_ids))


def test_empty():
    res = alifestd_mark_num_leaves_asexual(alifestd_make_empty())
    assert "num_leaves" in res
    assert len(res) == 0


@pytest.mark.parametrize("mutate", [True, False])
def test_simple1(mutate: bool):
    phylogeny_df = pd.DataFrame(
        {
            "id": [0, 1, 2],
            "ancestor_list": ["[None]", "[0]", "[1]"],
        }
    )
    original_df = phylogeny_df.copy()
    result_df = alifestd_mark_num_leaves_asexual(
        phylogeny_df,
        mutate=mutate,
    )
    assert result_df.loc[0, "num_leaves"] == 1
    assert result_df.loc[1, "num_leaves"] == 1
    assert result_df.loc[2, "num_leaves"] == 1

    if not mutate:
        assert original_df.equals(phylogeny_df)


@pytest.mark.parametrize("mutate", [True, False])
def test_simple2(mutate: bool):
    phylogeny_df = pd.DataFrame(
        {
            "id": [1, 0, 2, 3],
            "ancestor_list": ["[0]", "[None]", "[0]", "[1]"],
        }
    )
    original_df = phylogeny_df.copy()
    result_df = alifestd_mark_num_leaves_asexual(
        phylogeny_df,
        mutate=mutate,
    )
    result_df.index = result_df["id"]
    assert result_df.loc[1, "num_leaves"] == 1
    assert result_df.loc[0, "num_leaves"] == 2
    assert result_df.loc[2, "num_leaves"] == 1
    assert result_df.loc[3, "num_leaves"] == 1

    if not mutate:
        assert original_df.equals(phylogeny_df)


@pytest.mark.parametrize("mutate", [True, False])
def test_simple3(mutate: bool):
    phylogeny_df = pd.DataFrame(
        {
            "id": [1, 0, 2, 3],
            "ancestor_list": ["[None]", "[None]", "[0]", "[1]"],
        }
    )
    original_df = phylogeny_df.copy()
    result_df = alifestd_mark_num_leaves_asexual(
        phylogeny_df,
        mutate=mutate,
    )
    result_df.index = result_df["id"]
    assert result_df.loc[1, "num_leaves"] == 1
    assert result_df.loc[0, "num_leaves"] == 1
    assert result_df.loc[2, "num_leaves"] == 1
    assert result_df.loc[3, "num_leaves"] == 1

    if not mutate:
        assert original_df.equals(phylogeny_df)
