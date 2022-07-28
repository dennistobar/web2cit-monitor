from web2citwrapper import ResultElement, NoResultsError
from pytest import raises


def test_invalid_keys():
    with raises(NoResultsError):
        ResultElement({'el': 'x'}).result()


def test_invalid_content_key():
    with raises(NoResultsError):
        ResultElement({'results': 'x'}).result()


def test_invalid_count_key():
    with raises(NoResultsError):
        ResultElement({'results': []}).result()
