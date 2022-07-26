from web2citwrapper import Page
from pytest import fixture
import vcr


@fixture
def page_keys():
    return ['path', 'results', 'href', 'pattern']


@vcr.use_cassette('tests/vcr_cassetes/page-check.yml')
def test_page_check(page_keys):
    """Test an API call to some webpage non parsed"""

    page = Page(url='https://mediawiki.org')
    response = page.info()

    assert isinstance(response, list)
    item = response.pop()
    assert isinstance(item, dict)
    assert set(page_keys).issubset(item.keys())
    assert item['href'] == 'https://mediawiki.org/'


@vcr.use_cassette('tests/vcr_cassetes/page-check-test.yml')
def test_page_check_test(page_keys):
    """Test an API call to some webpage testing"""

    page = Page(url='https://mediawiki.org')
    response = page.tests()

    assert isinstance(response, list)
    item = response.pop()
    assert isinstance(item, dict)
    assert set(page_keys).issubset(item.keys())
    assert item['href'] == 'https://mediawiki.org/'


@vcr.use_cassette('tests/vcr_cassetes/page-check-test-score.yml')
def test_page_check_score():
    """Test an API call to some webpage testing"""

    url = 'https://www.elpais.com.uy/informacion/politica/lacalle-salio-cruce-diputado-mpp-dijo-hay-ola-robos-violentos.html'

    page = Page(url=url)
    response = page.score()

    assert isinstance(response, dict)
    assert isinstance(response.get(url), list)
