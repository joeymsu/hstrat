from hstrat import hstrat


def test_deposition():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    assert store1.GetNumStrataRetained() == 0

    stratum1 = hstrat.HereditaryStratum(deposition_rank=0)
    store1.DepositStratum(0, stratum1)
    assert store1.GetNumStrataRetained() == 1
    assert store1.GetStratumAtColumnIndex(0) == stratum1

    store2 = store1.Clone()

    stratum2 = hstrat.HereditaryStratum(deposition_rank=1)
    store1.DepositStratum(1, stratum2)
    assert store1.GetNumStrataRetained() == 2
    assert store1.GetStratumAtColumnIndex(1) == stratum2
    assert store1.GetStratumAtColumnIndex(0) != stratum2

    assert store2.GetNumStrataRetained() == 1
    assert store2.GetStratumAtColumnIndex(0) == stratum1


def test_deletion1():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    stratum1 = hstrat.HereditaryStratum(deposition_rank=0)
    store1.DepositStratum(0, stratum1)

    store2 = store1.Clone()
    stratum2 = hstrat.HereditaryStratum(deposition_rank=1)
    store1.DepositStratum(1, stratum2)

    del store1
    assert store2.GetNumStrataRetained() == 1
    assert store2.GetStratumAtColumnIndex(0) == stratum1


def test_deletion2():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    stratum1 = hstrat.HereditaryStratum(deposition_rank=0)
    store1.DepositStratum(0, stratum1)

    store2 = store1.Clone()
    stratum2 = hstrat.HereditaryStratum(deposition_rank=1)
    store1.DepositStratum(1, stratum2)

    del store2
    assert store1.GetNumStrataRetained() == 2
    assert store1.GetStratumAtColumnIndex(0) == stratum1
    assert store1.GetStratumAtColumnIndex(1) == stratum2


def test_equality():
    assert (
        hstrat.HereditaryStratumOrderedStoreList()
        == hstrat.HereditaryStratumOrderedStoreList()
    )

    store1 = hstrat.HereditaryStratumOrderedStoreList()
    store1.DepositStratum(0, hstrat.HereditaryStratum(deposition_rank=0))
    store2 = store1.Clone()
    assert store1 == store2

    store2.DepositStratum(1, hstrat.HereditaryStratum(deposition_rank=1))
    assert store1 != store2


def test_GetRankAtColumnIndex():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    store1.DepositStratum(0, hstrat.HereditaryStratum(deposition_rank=0))
    store1.DepositStratum(1, hstrat.HereditaryStratum(deposition_rank=1))
    store1.DepositStratum(2, hstrat.HereditaryStratum(deposition_rank=2))
    assert store1.GetRankAtColumnIndex(0) == 0
    assert store1.GetRankAtColumnIndex(1) == 1
    assert store1.GetRankAtColumnIndex(2) == 2

    store1.DelRanks([1])
    assert store1.GetRankAtColumnIndex(0) == 0
    assert store1.GetRankAtColumnIndex(1) == 2


def test_GetStratumAtColumnIndex():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    strata = [
        hstrat.HereditaryStratum(deposition_rank=rank) for rank in range(3)
    ]
    for rank, stratum in enumerate(strata):
        store1.DepositStratum(rank, stratum)

    for rank, stratum in enumerate(strata):
        assert store1.GetStratumAtColumnIndex(rank) == strata[rank]

    store1.DelRanks([1])
    assert store1.GetStratumAtColumnIndex(0) == strata[0]
    assert store1.GetStratumAtColumnIndex(1) == strata[2]


def test_GetNumStrataRetained():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    for rank in range(5):
        assert store1.GetNumStrataRetained() == rank
        store1.DepositStratum(rank, hstrat.HereditaryStratum())
    assert store1.GetNumStrataRetained() == 5

    store1.DelRanks([1, 2], get_column_index_of_rank=lambda x: x)
    assert store1.GetNumStrataRetained() == 3

    store1.DepositStratum(5, hstrat.HereditaryStratum())
    assert store1.GetNumStrataRetained() == 4

    store1.DelRanks(
        [5],
        get_column_index_of_rank=lambda x: {
            3: 0,
            5: 1,
        }[x],
    )
    assert store1.GetNumStrataRetained() == 3


def test_GetColumnIndexOfRank():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 63]
    for rank in ranks:
        store1.DepositStratum(
            rank=rank,
            stratum=hstrat.HereditaryStratum(deposition_rank=rank),
        )

    assert store1.GetColumnIndexOfRank(-1) is None
    assert store1.GetColumnIndexOfRank(0) == 0
    assert store1.GetColumnIndexOfRank(1) is None
    assert store1.GetColumnIndexOfRank(8) == 1
    assert store1.GetColumnIndexOfRank(42) == 2
    assert store1.GetColumnIndexOfRank(63) == 3
    assert store1.GetColumnIndexOfRank(64) is None


def test_IterRetainedRanks():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 63]
    for rank in ranks:
        store1.DepositStratum(
            rank=rank,
            stratum=hstrat.HereditaryStratum(deposition_rank=rank),
        )

    assert set(store1.IterRetainedRanks()) == set(ranks)


def test_IterRankDifferentia1():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 63]
    strata = [hstrat.HereditaryStratum(deposition_rank=rank) for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    assert [*zip(ranks, [stratum.GetDifferentia() for stratum in strata])] == [
        *store1.IterRankDifferentia()
    ]
    assert [*zip(ranks, [stratum.GetDifferentia() for stratum in strata])][
        0:
    ] == [*store1.IterRankDifferentia(start_column_index=0)]
    assert [*zip(ranks, [stratum.GetDifferentia() for stratum in strata])][
        2:
    ] == [*store1.IterRankDifferentia(start_column_index=2)]


def test_IterRankDifferentia2():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 63]
    strata = [hstrat.HereditaryStratum(deposition_rank=rank) for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    def col_index_to_rank(column_idx):
        return ranks[column_idx]

    assert [*zip(ranks, [stratum.GetDifferentia() for stratum in strata])] == [
        *store1.IterRankDifferentia(
            get_rank_at_column_index=col_index_to_rank,
        )
    ]
    assert [*zip(ranks, [stratum.GetDifferentia() for stratum in strata])][
        0:
    ] == [
        *store1.IterRankDifferentia(
            get_rank_at_column_index=col_index_to_rank,
            start_column_index=0,
        )
    ]
    assert [*zip(ranks, [stratum.GetDifferentia() for stratum in strata])][
        2:
    ] == [
        *store1.IterRankDifferentia(
            get_rank_at_column_index=col_index_to_rank,
            start_column_index=2,
        )
    ]


def test_DelRanks_getrank_impl1():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63]
    strata = [hstrat.HereditaryStratum(deposition_rank=rank) for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [8, 42],
        [],
        [55],
        [],
        [0, 63],
        [],
    ):
        store1.DelRanks(deletion)
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [*store1.IterRankDifferentia()]


def test_DelRanks_getrank_impl2():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63]
    strata = [hstrat.HereditaryStratum(deposition_rank=rank) for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [0, 63],
        [],
        [8],
        [],
        [55],
        [],
        [42],
        [],
    ):
        store1.DelRanks(deletion)
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [*store1.IterRankDifferentia()]


def test_DelRanks_getrank_impl3():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63, 80]
    strata = [hstrat.HereditaryStratum(deposition_rank=rank) for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [0, 80],
        [],
        [63],
        [],
        [8, 55],
        [],
        [42],
        [],
    ):
        store1.DelRanks(deletion)
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [*store1.IterRankDifferentia()]


def test_DelRanks_getrank_impl4():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63]
    strata = [hstrat.HereditaryStratum(deposition_rank=rank) for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [55, 63],
        [],
        [0, 8],
        [],
        [42],
        [],
    ):
        store1.DelRanks(deletion)
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [*store1.IterRankDifferentia()]


def test_DelRanks_getrank_impl5():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63]
    strata = [hstrat.HereditaryStratum(deposition_rank=rank) for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [42, 63],
        [],
        [0, 8, 55],
        [],
    ):
        store1.DelRanks(deletion)
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [*store1.IterRankDifferentia()]


def test_DelRanks_calcrank_impl1():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63]
    strata = [hstrat.HereditaryStratum() for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [8, 42],
        [],
        [55],
        [],
        [0, 63],
        [],
    ):
        store1.DelRanks(
            get_column_index_of_rank=lambda rank: ranks.index(rank),
            ranks=deletion,
        )
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [
            *store1.IterRankDifferentia(
                get_rank_at_column_index=lambda idx: ranks[idx],
            )
        ]


def test_DelRanks_calcrank_impl2():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63]
    strata = [hstrat.HereditaryStratum() for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [0, 63],
        [],
        [8],
        [],
        [55],
        [],
        [42],
        [],
    ):
        store1.DelRanks(
            get_column_index_of_rank=lambda rank: ranks.index(rank),
            ranks=deletion,
        )
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [
            *store1.IterRankDifferentia(
                get_rank_at_column_index=lambda idx: ranks[idx],
            )
        ]


def test_DelRanks_calcrank_impl3():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63, 80]
    strata = [hstrat.HereditaryStratum() for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [0, 80],
        [],
        [63],
        [],
        [8, 55],
        [],
        [42],
        [],
    ):
        store1.DelRanks(
            get_column_index_of_rank=lambda rank: ranks.index(rank),
            ranks=deletion,
        )
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [
            *store1.IterRankDifferentia(
                get_rank_at_column_index=lambda idx: ranks[idx],
            )
        ]


def test_DelRanks_calcrank_impl4():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63]
    strata = [hstrat.HereditaryStratum() for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [55, 63],
        [],
        [0, 8],
        [],
        [42],
        [],
    ):
        store1.DelRanks(
            get_column_index_of_rank=lambda rank: ranks.index(rank),
            ranks=deletion,
        )
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [
            *store1.IterRankDifferentia(
                get_rank_at_column_index=lambda idx: ranks[idx],
            )
        ]


def test_DelRanks_calcrank_impl5():
    store1 = hstrat.HereditaryStratumOrderedStoreList()
    ranks = [0, 8, 42, 55, 63]
    strata = [hstrat.HereditaryStratum() for rank in ranks]
    for rank, stratum in zip(ranks, strata):
        store1.DepositStratum(rank=rank, stratum=stratum)

    for deletion in (
        [],
        [42, 63],
        [],
        [0, 8, 55],
        [],
    ):
        store1.DelRanks(
            get_column_index_of_rank=lambda rank: ranks.index(rank),
            ranks=deletion,
        )
        for rank in deletion:
            del strata[ranks.index(rank)]
            ranks.remove(rank)
        assert [
            *zip(ranks, [stratum.GetDifferentia() for stratum in strata])
        ] == [
            *store1.IterRankDifferentia(
                get_rank_at_column_index=lambda idx: ranks[idx],
            )
        ]
