from pytest import raises
from web2citwrapper import comm


def test_no_url():
    with raises(comm.URLMissingError):
        comm.get()
