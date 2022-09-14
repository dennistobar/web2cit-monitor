import os
from time import time
from web2citwrapper import URL, Domain
from writer import write_detailed, write_main_log
from monitor import Prefix
from web2citwrapper import Domain
from web2citwrapper.comm import Web2CitError
from web2citwrapper.element_base import NoResultsError
import pywikibot


class DomainWriter(object):

    def __init__(self, domain: str, log: bool = False):
        self.domain = domain
        self.has_log = log
        self.site = pywikibot.Site("meta", "meta")
        self.prefix = 'Web2Cit/monitor/checks/'

    def write(self):
        if self.domain is None:
            raise Web2CitError('Domain not defined')

        try:
            domain = Domain(self.domain)
            page_base = self.get_page(domain.get_domain_to_meta(), 'results')
            page_base_log = self.get_page(domain.get_domain_to_meta(), 'log')

            results_text = write_detailed(domain)
            log_text = write_main_log(domain)

            if self.has_log is True:
                self.write_log(domain, page_base_log)
                print('Log write: {}'.format(self.domain))
            if self.has_log is False:
                self.write_meta(page_base, results_text)
                self.write_meta(page_base_log, log_text)
                print('Meta write: {}'.format(self.domain))

        except Web2CitError as e:
            print('[!] {} error {}'.format(self.domain, e))
        except NoResultsError as e:
            print('[!] {} error {}'.format(self.domain, e))

    def write_log(self, domain: dict, page_base_log: pywikibot.Page):
        """
        Writes the log file.
        """
        with open(os.path.join('./logs/domains/{}.log'.format(self.domain)), 'w') as file:
            file.write(write_detailed(domain))
        with open(os.path.join('./logs/logs/{}.log'.format(self.domain)), 'w') as file:
            file.write(write_main_log(domain,
                                      trigger='manual',
                                      previous_text=page_base_log.text))

    def write_meta(self, page: pywikibot.Page, text: str,
                   summary: str = 'Update domain check'):
        page.put(text, summary=summary, botflag=True)

    def get_page(self, domain: str, type: str) -> pywikibot.Page:
        """
        Gets the page of the given type.
        """
        return pywikibot.Page(self.site, self.prefix + domain + '/' + type)
