from web2citwrapper import Domain
from datetime import datetime
from mako.template import Template


def write_main_log(domain: Domain, why: str = 'programmed'):
    """
    Writes the main log file for the given domain.
    """
    tests_counted = domain.tests_counted()
    score = round(domain.score(), 4)*100
    templates = domain.get_config('templates')
    patterns = domain.get_config('patterns')
    tests = domain.get_config('tests')

    row = ("|-\n| {0} || {1} || {2} || {3}%".format(
        datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S%z'), why, tests_counted,
        score))

    for element in [templates, patterns, tests]:
        if element == '-':
            row += (' || -')
        else:
            row += (
                ' || [[Special:Special:PermanentLink/{0}|{0}]]'.format(element))

    return row


def write_detailed(domain: Domain) -> str:
    """
    Writes the detailed log file for the given domain.
    """
    paths = list(domain.retrieve())
    base = Template(filename='./templates/base.txt')
    return base.render(domain_name=domain.value.get(
        'domain'), paths=paths)
