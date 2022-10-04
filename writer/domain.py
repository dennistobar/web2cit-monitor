import os
from random import random
from time import sleep
from web2citwrapper import Domain
from writer import write_detailed, write_main_log
from web2citwrapper import Domain
from web2citwrapper.comm import Web2CitError
from web2citwrapper.element_base import NoResultsError
import pywikibot


class DomainWriter(object):

    def __init__(self, domain: str, log: bool = False, trigger: str = 'programmed'):
        self.domain = domain
        self.has_log = log
        self.site = pywikibot.Site("meta", "meta")
        self.trigger = trigger
        self.prefix = 'Web2Cit/monitor/'

    def write(self):
        if self.domain is None:
            raise Web2CitError('Domain not defined')

        try:
            domain = Domain(self.domain)
            page_base = self.get_page(domain.get_domain_to_meta(), 'results')
            page_base_log = self.get_page(domain.get_domain_to_meta(), 'log')

            results_text = write_detailed(domain)
            log_text = write_main_log(
                domain, trigger=self.trigger, previous_text=page_base_log.text)

            if self.has_log is True:
                self.write_log('domain', results_text)
                self.write_log('logs', log_text)
                print('Log write: {}'.format(self.domain))
            if self.has_log is False:
                self.write_meta(page_base, results_text)
                self.write_meta(page_base_log, log_text)
                print('Meta write: {}'.format(self.domain))

        except Web2CitError as e:
            print('[!] {} error {}'.format(self.domain, e))
        except NoResultsError as e:
            print('[!] {} error {}'.format(self.domain, e))

    def write_log(self, type: str, text: str):
        """
        Writes the log file.
        """
        with open(os.path.join('./logs/{}/{}.log'.format(type, self.domain)), 'w') as file:
            file.write(text)

    def write_meta(self, page: pywikibot.Page, text: str,
                   summary: str = 'Update domain check'):
        sleep(random() % 30)
        page.put(text, summary=summary, botflag=True)

    def get_page(self, domain: str, type: str) -> pywikibot.Page:
        """
        Gets the page of the given type.
        """
        return pywikibot.Page(self.site, self.prefix + domain + '/' + type)
