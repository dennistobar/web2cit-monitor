from pytest import raises
from web2citwrapper import comm


def test_no_url():
    with raises(comm.ParametersMissinError):
        comm.get()


def test_error_url():
    with raises(comm.Web2CitError):
        comm.get({'ulr': 'invalid'})
