import pandas as pd


def alifestd_is_disconnected(phylogeny_df: pd.DataFrame) -> bool:
    return (
        (phylogeny_df["ancestor_list"] == "[]").sum()
        + (phylogeny_df["ancestor_list"] == "[NONE]").sum()
        + (phylogeny_df["ancestor_list"] == "[none]").sum()
        + (phylogeny_df["ancestor_list"] == "[None]").sum()
    ) >= 2
