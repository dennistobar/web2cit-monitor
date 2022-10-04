import os
from time import time
from web2citwrapper import URL, Domain
from writer import write_detailed, write_main_log
from monitor import Prefix
from web2citwrapper import Domain
from web2citwrapper.comm import Web2CitError
from web2citwrapper.element_base import NoResultsError
import pywikibot

pf = Prefix()
for domain_name in pf.run():
    try:
        domain = Domain(domain_name)
        page_base = pywikibot.Page(pywikibot.Site(
            "meta", "meta"), 'Web2cit/monitor/' + domain.get_domain_to_meta() + '/results')
        page_base_log = pywikibot.Page(pywikibot.Site(
            "meta", "meta"), 'Web2cit/monitor/' + domain.get_domain_to_meta() + '/log')
        print(domain.get_domain_to_meta())
        with open(os.path.join('./logs/domains/{}.log'.format(domain_name)), 'w') as file:
            file.write(write_detailed(domain))
        with open(os.path.join('./logs/logs/{}.log'.format(domain_name)), 'w') as file:
            file.write(write_main_log(domain))

    except Web2CitError as e:
        print('[!] {} error {}'.format(domain_name, e))
    except Exception as e:
        print(e)

# page = pywikibot.Page(pywikibot.Site('meta', 'meta'),
#                       title='User:Superzerocool/Test')
# page.put('Testing', summary='Testing put')
