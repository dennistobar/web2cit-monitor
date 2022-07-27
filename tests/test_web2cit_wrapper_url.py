from web2citwrapper import Result, URL
from pytest import raises
import vcr


@vcr.use_cassette('tests/vcr_cassetes/url_no_parsed.yml')
def test_url_no_parsed():
    with raises(Exception):
        """Test an API call to some webpage non parsed"""

        page = URL(url='https://mediawiki.org')
        response = page.retrieve()

        assert isinstance(response, Result)
        assert response.href() == 'https://mediawiki.org/'
        assert isinstance(response.result(), dict)
        # Exception, not have fields!
        assert isinstance(response.fields(), list)
        assert isinstance(response.score(), float)
        assert isinstance(response.path(), str)


@vcr.use_cassette('tests/vcr_cassetes/url_parsed.yml')
def test_url_parsed():
    """Test an API call to some webpage parsed"""

    page = URL(url='https://www.elpais.com.uy/informacion/politica/lacalle-salio-cruce-diputado-mpp-dijo-hay-ola-robos-violentos.html')
    response = page.retrieve()

    assert isinstance(response, Result)
    assert response.href() == 'https://www.elpais.com.uy/informacion/politica/lacalle-salio-cruce-diputado-mpp-dijo-hay-ola-robos-violentos.html'
    assert isinstance(response.path(), str)
    assert isinstance(response.result(), dict)
    assert isinstance(response.fields(), list)
    assert isinstance(response.score(), float)


def test_url_parse_no_data():
    """Test parsing an URL with errors"""
    with raises(Exception):
        page = URL('dummy')
        page._parse_response({})


def test_url_parse_no_target():
    """Test parsing an URL with errors"""
    with raises(Exception):
        page = URL('dummy')
        page._parse_response({'data': {}})
