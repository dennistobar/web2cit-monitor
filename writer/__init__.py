from web2citwrapper import Domain
from datetime import datetime
from mako.template import Template
from mako.lookup import TemplateLookup
import re
import pywikibot


def write_logs(domain: Domain, trigger: str = 'programmed', previous_text: str = '') -> str:
    """
    Writes the main log file for the given domain.
    """
    tests_counted = domain.tests_counted()
    if isinstance(domain.score(), str):
        score = 'n/d'
    else:
        score = round(domain.score(), 4)*100
    templates = domain.get_config('templates')
    patterns = domain.get_config('patterns')
    tests = domain.get_config('tests')

    try:
        site = pywikibot.Site('meta', 'meta')
        page = pywikibot.Page(
            site, 'Web2Cit/monitor/{}/results'.format(domain.get_domain_to_meta()))
        rev_id = page.latest_revision_id
    except:
        rev_id = 0

    mylookup = TemplateLookup(directories=['.', 'templates'])
    log = Template(filename='templates/log.txt', lookup=mylookup)

    text = """
{{{{ Web2Cit/log/row
| timestamp = {0}
| trigger = {1}
| tests_run = {2}
| avg_score = {3}
| templates_rev_id = {4}
| patterns_rev_id = {5}
| tests_rev_id = {6}
| results_rev_id = {7}
    }}}}
|-""".format(
        datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S%z'), trigger,
        tests_counted, score, templates, patterns, tests, rev_id)

    # Obtain the latest check
    past = re.search(r"<onlyinclude>(.*)<\/onlyinclude>",
                     previous_text, re.DOTALL | re.MULTILINE)

    # Obtain the past checks
    older = re.search(r"<noinclude>(.*)<\/noinclude>",
                      previous_text, re.DOTALL | re.MULTILINE)

    # Join all groups if exists
    past_text = "\n|-\n".join(past.groups()) if past is not None else ''
    older_text = "\n".join(older.groups()) if older is not None else ''

    # Join in a new text
    old_text = past_text + '\n' + older_text
    old_text = re.sub(r'\n{2,}', '\n', old_text, re.DOTALL | re.MULTILINE)

    return str(log.render(new_text=text, old_text=old_text))


def write_results(domain: Domain) -> str:
    """
    Writes the detailed results for the given domain.
    """
    paths = list(domain.retrieve())
    mylookup = TemplateLookup(directories=['.', 'templates'])
    base = Template(filename='templates/base.txt', lookup=mylookup)
    return str(base.render(domain_name=domain.value.get(
        'domain'), paths=paths))
