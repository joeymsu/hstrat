import os

import pandas as pd
import pytest

from hstrat._auxiliary_lib import (
    alifestd_is_topologically_sorted,
    alifestd_parse_ancestor_ids,
    alifestd_topological_sort,
    swap_rows_and_indices,
)

assets_path = os.path.join(os.path.dirname(__file__), "assets")


@pytest.mark.parametrize(
    "phylogeny_df",
    [
        pd.read_csv(f"{assets_path}/nk_ecoeaselection.csv"),
        pd.read_csv(f"{assets_path}/nk_lexicaseselection.csv"),
        pd.read_csv(f"{assets_path}/nk_tournamentselection.csv"),
    ],
)
def test_alifestd_topological_sort_empty(phylogeny_df):
    phylogeny_df.sort_values("id", ascending=True, inplace=True)
    phylogeny_df_ = phylogeny_df.copy()

    operand = phylogeny_df.iloc[-1:0, :]
    res = alifestd_topological_sort(operand)
    assert alifestd_is_topologically_sorted(res)
    assert len(res) == len(operand)
    # ensure no side effects
    assert phylogeny_df.equals(phylogeny_df_)


@pytest.mark.parametrize(
    "phylogeny_df",
    [
        pd.read_csv(f"{assets_path}/nk_ecoeaselection.csv"),
        pd.read_csv(f"{assets_path}/nk_lexicaseselection.csv"),
        pd.read_csv(f"{assets_path}/nk_tournamentselection.csv"),
    ],
)
def test_alifestd_topological_sort_singleton(phylogeny_df):
    phylogeny_df.sort_values("id", ascending=True, inplace=True)
    phylogeny_df_ = phylogeny_df.copy()

    operand = phylogeny_df.iloc[0:1, :]
    res = alifestd_topological_sort(operand)
    assert alifestd_is_topologically_sorted(res)
    assert len(res) == len(operand)
    # ensure no side effects
    assert phylogeny_df.equals(phylogeny_df_)


def test_alifestd_topological_sort_tworoots():

    phylo1 = pd.read_csv(f"{assets_path}/nk_ecoeaselection.csv")
    phylo1.sort_values("id", ascending=True, inplace=True)
    phylo2 = pd.read_csv(f"{assets_path}/nk_lexicaseselection.csv")
    phylo2.sort_values("id", ascending=True, inplace=True)

    operand = pd.concat(
        [
            phylo1.iloc[0:1, :],
            phylo2.iloc[0:1, :],
        ]
    )
    res = alifestd_topological_sort(operand)
    assert alifestd_is_topologically_sorted(res)
    assert len(res) == len(operand)


@pytest.mark.parametrize(
    "phylogeny_df",
    [
        pd.read_csv(f"{assets_path}/nk_ecoeaselection.csv"),
        pd.read_csv(f"{assets_path}/nk_lexicaseselection.csv"),
        pd.read_csv(f"{assets_path}/nk_tournamentselection.csv"),
    ],
)
def test_alifestd_topological_sort_twolineages(phylogeny_df):

    phylogeny_df.sort_values("id", ascending=True, inplace=True)
    phylogeny_df.reset_index(inplace=True)
    max_id = phylogeny_df["id"].max()

    lineage1 = phylogeny_df.copy()
    lineage2 = phylogeny_df.copy()
    lineage2["id"] += max_id
    lineage2["ancestor_list"] = lineage2["ancestor_list"].apply(
        lambda ancestor_list_str: str(
            [
                ancestor_id + max_id
                for ancestor_id in alifestd_parse_ancestor_ids(
                    ancestor_list_str
                )
            ]
        )
    )

    operand = pd.concat(
        [
            lineage1.iloc[::-1, :],
            lineage2,
        ]
    )
    res = alifestd_topological_sort(operand)
    assert alifestd_is_topologically_sorted(res)
    assert len(res) == len(operand)

    operand = pd.concat(
        [
            lineage1.iloc[:10:-1, :],
            lineage2,
            lineage1.iloc[10::-1, :],
        ]
    )
    res = alifestd_topological_sort(operand)
    assert alifestd_is_topologically_sorted(res)
    assert len(res) == len(operand)

    operand = pd.concat(
        [
            lineage1.iloc[10::, :],
            lineage2,
            lineage1.iloc[:10:, :],
        ]
    )
    res = alifestd_topological_sort(operand)
    assert alifestd_is_topologically_sorted(res)
    assert len(res) == len(operand)


@pytest.mark.parametrize(
    "phylogeny_df",
    [
        pd.read_csv(f"{assets_path}/nk_ecoeaselection.csv"),
        pd.read_csv(f"{assets_path}/nk_lexicaseselection.csv"),
        pd.read_csv(f"{assets_path}/nk_tournamentselection.csv"),
    ],
)
def test_alifestd_topological_sort(phylogeny_df):
    phylogeny_df.sort_values("id", ascending=False, inplace=True)
    phylogeny_df.set_index("id", drop=False, inplace=True)
    phylogeny_df_ = phylogeny_df.copy()

    operand = phylogeny_df
    res = alifestd_topological_sort(operand)
    assert alifestd_is_topologically_sorted(res)
    assert len(res) == len(operand)
    # check for side effects
    assert phylogeny_df.equals(phylogeny_df_)

    # reverse dataframe
    phylogeny_df = phylogeny_df.iloc[::-1]
    phylogeny_df_ = phylogeny_df.copy()
    assert alifestd_is_topologically_sorted(phylogeny_df)

    # one-by-one transpositions
    for idx, row in phylogeny_df.sample(10).iterrows():
        for ancestor_id in alifestd_parse_ancestor_ids(row["ancestor_list"]):
            operand = swap_rows_and_indices(phylogeny_df, idx, ancestor_id)
            res = alifestd_topological_sort(operand)
            assert alifestd_is_topologically_sorted(res)
            assert len(res) == len(operand)
            # check for side effects
            assert phylogeny_df.equals(phylogeny_df_)

    # cumulative transpositions in random order
    for idx, row in phylogeny_df.sample(10).iterrows():
        for ancestor_id in alifestd_parse_ancestor_ids(row["ancestor_list"]):
            assert ancestor_id in phylogeny_df_.index
            phylogeny_df = swap_rows_and_indices(
                phylogeny_df, idx, ancestor_id
            )
            res = alifestd_topological_sort(operand)
            assert alifestd_is_topologically_sorted(res)
            assert len(res) == len(operand)
