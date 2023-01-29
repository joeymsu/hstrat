import pandas as pd

from ._alifestd_is_sexual import alifestd_is_sexual


def alifestd_is_asexual(phylogeny_df: pd.DataFrame) -> bool:
    """Do all organisms in the phylogeny have one or no immediate ancestor?"""
    return not alifestd_is_sexual(phylogeny_df)
