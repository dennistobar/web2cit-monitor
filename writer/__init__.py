from web2citwrapper import Domain
from datetime import datetime
from mako.template import Template
from mako.lookup import TemplateLookup


def write_main_log(domain: Domain, trigger: str = 'programmed'):
    """
    Writes the main log file for the given domain.
    """
    tests_counted = domain.tests_counted()
    if domain.score() is None:
        score = '?'
    else:
        score = round(domain.score(), 4)*100
    templates = domain.get_config('templates')
    patterns = domain.get_config('patterns')
    tests = domain.get_config('tests')

    text = """{{{{ Web2Cit/monitor/log/row
    | timestamp = {0}
    | trigger = {1}
    | tests_run = {2}
    | avg_score = {3}
    | templates_rev_id = {4}
    | patterns_rev_id = {5}
    | tests_rev_id = {6}
    }}}}""".format(
        datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S%z'), trigger,
        tests_counted, score, templates, patterns, tests)

    return text


def write_detailed(domain: Domain) -> str:
    """
    Writes the detailed log file for the given domain.
    """
    paths = list(domain.retrieve())
    mylookup = TemplateLookup(directories=['.', 'templates'])
    base = Template(filename='templates/base.txt', lookup=mylookup)
    return base.render(domain_name=domain.value.get(
        'domain'), paths=paths)
