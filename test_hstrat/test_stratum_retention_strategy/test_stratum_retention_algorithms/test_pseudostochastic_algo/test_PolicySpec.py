import pytest

from hstrat.hstrat import pseudostochastic_algo


@pytest.mark.parametrize(
    "hash_salt",
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
def test_eq(hash_salt):
    spec = pseudostochastic_algo.PolicySpec(hash_salt)
    assert spec == spec
    assert spec == pseudostochastic_algo.PolicySpec(hash_salt)
    assert not spec == pseudostochastic_algo.PolicySpec(hash_salt + 1)


@pytest.mark.parametrize(
    "hash_salt",
    [
        1,
        2,
        3,
        7,
        42,
        100,
    ],
)
def test_GetHashSalt(hash_salt):
    spec = pseudostochastic_algo.PolicySpec(hash_salt)
    assert spec.GetHashSalt() == hash_salt


def test_GetAlgoName():
    hash_salt = 1
    spec = pseudostochastic_algo.PolicySpec(hash_salt)
    assert spec.GetAlgoName()


def test_GetAlgoTitle():
    hash_salt = 1
    spec = pseudostochastic_algo.PolicySpec(hash_salt)
    assert spec.GetAlgoTitle()


def test_repr():
    hash_salt = 1
    spec = pseudostochastic_algo.PolicySpec(hash_salt)
    assert str(hash_salt) in repr(spec)
    assert spec.GetAlgoName() in repr(spec)


def test_str():
    hash_salt = 1
    spec = pseudostochastic_algo.PolicySpec(hash_salt)
    assert str(hash_salt) in str(spec)
    assert spec.GetAlgoTitle() in str(spec)
