#!/bin/python3

from copy import deepcopy
import random
import unittest

from pylib import RankLabeledHereditaryStratum

random.seed(1)


class TestRankLabeledHereditaryStratum(unittest.TestCase):

    def test_deposition_rank(self):
        assert RankLabeledHereditaryStratum(
            deposition_rank=42,
        ).GetDepositionRank() == 42

    def test_uid_generation(self):
        original1 = RankLabeledHereditaryStratum(
            deposition_rank=42,
        )
        copy1 = deepcopy(original1)
        original2 = RankLabeledHereditaryStratum(
            deposition_rank=42,
        )

        assert original1 == copy1
        assert original1 != original2
        assert copy1 != original2

        assert original1.GetUid() == copy1.GetUid()
        assert original1.GetUid() != original2.GetUid()
        assert copy1.GetUid() != original2.GetUid()


if __name__ == '__main__':
    unittest.main()
