from web2citwrapper import Domain, NoResultsError
from pytest import raises


def test_url_parse_no_data():
    """Test parsing an URL with errors"""
    with raises(NoResultsError):
        page = Domain('dummy')
        page._parse_response({})


def test_url_parse_no_target():
    """Test parsing an URL with errors"""
    with raises(NoResultsError):
        page = Domain('dummy')
        page._parse_response({'data': {}})


def test_url_parse_incorrect_target():
    """Test parsing an URL with errors"""
    with raises(NoResultsError):
        page = Domain('dummy')
        page._parse_response({'data': {'targets': 'x'}})


def test_url_parse_len_target():
    """Test parsing an URL with errors"""
    with raises(NoResultsError):
        page = Domain('dummy')
        page._parse_response({'data': {'targets': []}})
