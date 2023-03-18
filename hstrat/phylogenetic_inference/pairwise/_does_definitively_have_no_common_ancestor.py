from ..._auxiliary_lib import HereditaryStratigraphicArtifact
from ...juxtaposition import (
    calc_definitive_max_rank_of_first_retained_disparity_between,
)


def does_definitively_have_no_common_ancestor(
    first: HereditaryStratigraphicArtifact,
    second: HereditaryStratigraphicArtifact,
) -> bool:
    """Does the hereditary stratigraphic record definitively prove that first
    and second could not possibly share a common ancestor?

    If the founding strata of first and second (i.e., generation 0) have
    unequal differentia, then first and second cannot possibly share common
    ancestry.

    Note equal differentia at generation 0 does not necessarily imply common
    ancestry; colliding differentia values could have been independently
    generated by chance.

    Note also that stratum rention policies are strictly required to permanently
    retain the most ancient stratum.

    See Also
    --------
    does_have_any_common_ancestor:
        Can we conclude with confidence_level confidence that first and second
        share a common ancestor?
    """
    first_disparity = (
        calc_definitive_max_rank_of_first_retained_disparity_between(
            first,
            second,
        )
    )
    return False if first_disparity is None else first_disparity == 0
