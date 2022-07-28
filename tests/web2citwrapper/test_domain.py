import types
from web2citwrapper import ResultElement, Domain
from pytest import raises
import vcr


@vcr.use_cassette('tests/vcr_cassetes/domain_no_parsed.yml')
def test_domain_no_parsed():
    """Test an API call to some domain non parsed"""
    with raises(Exception):
        page = Domain('https://mediawiki.org')
        response = page.retrieve()
        next(response)

        assert isinstance(response, types.GeneratorType)


@vcr.use_cassette('tests/vcr_cassetes/domain_parsed.yml')
def test_domain_parsed():
    """Test an API call to some domain parsed"""

    page = Domain('www.elobservador.com.uy')
    responses = page.retrieve()

    assert isinstance(responses, types.GeneratorType)
    for response in responses:
        assert isinstance(response, ResultElement)


def test_domain_parse_no_data():
    """Test parsing an URL with errors"""
    with raises(Exception):
        page = Domain(domain='dummy')
        page._parse_response({})


def test_domain_parse_no_target():
    """Test parsing an URL with errors"""
    with raises(Exception):
        page = Domain(domain='dummy')
        page._parse_response({'data': {}})
