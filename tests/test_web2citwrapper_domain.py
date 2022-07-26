from web2citwrapper import Domain
from pytest import raises
import vcr


@vcr.use_cassette('tests/vcr_cassetes/domain-test-valid.yml')
def test_domain_test():
    """Test an API call to a valid domain"""

    domain = Domain(domain='www.lavoz.com.ar')
    response = domain.tests()

    assert isinstance(response, list)
    item = response.pop()
    assert isinstance(item, dict)


@vcr.use_cassette('tests/vcr_cassetes/domain-test-valid.yml')
def test_domain_score():
    """Test an API call to a valid domain to get scores"""
    domain = Domain(domain='www.lavoz.com.ar')
    response = domain.score()

    assert isinstance(response, dict)
    key, value = response.popitem()
    assert isinstance(key, str)
    assert isinstance(value, list)


@vcr.use_cassette('tests/vcr_cassetes/domain-test-invalid.yml')
def test_invalid_domain_test():
    """Test an API call to an invalid domain"""
    with raises(Exception):
        domain = Domain(domain='notexists.com.asdfg')
        domain.tests()
