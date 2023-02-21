"""Frozen representations of genome annotations for efficient postprocessing
and analysis."""

from ._HereditaryStratigraphicAssemblageSpecimen import (
    HereditaryStratigraphicAssemblageSpecimen,
)
from ._HereditaryStratigraphicSpecimen import HereditaryStratigraphicSpecimen

# adapted from https://stackoverflow.com/a/31079085
__all__ = [
    "HereditaryStratigraphicAssemblageSpecimen",
    "HereditaryStratigraphicSpecimen",
]

from .._auxiliary_lib import launder_impl_modules as _launder

_launder(
    [
        HereditaryStratigraphicAssemblageSpecimen,
        HereditaryStratigraphicSpecimen,
    ],
    __name__,
)
del _launder  # prevent name from leaking
