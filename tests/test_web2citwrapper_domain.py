from web2citwrapper import Domain
from pytest import fixture, raises
import vcr


@fixture
def page_keys():
    return ['path', 'results', 'href', 'pattern']


@vcr.use_cassette('tests/vcr_cassetes/domain-test-valid.yml')
def test_domain_test(page_keys):
    """Test an API call to a valid domain"""

    domain = Domain(domain='www.lavoz.com.ar')
    response = domain.tests()

    assert isinstance(response, list)
    item = response.pop()
    assert isinstance(item, dict)
    assert set(page_keys).issubset(item.keys())


@vcr.use_cassette('tests/vcr_cassetes/domain-test-invalid.yml')
def test_invalid_domain_test(page_keys):
    """Test an API call to an invalid domain"""
    with raises(Exception):
        domain = Domain(domain='notexists.com.asdfg')
        domain.tests()
