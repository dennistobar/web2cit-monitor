import datetime
from typing import Iterable, Set
import pywikibot
from pywikibot import pagegenerators, Page
from web2citwrapper import Domain


class Prefix(object):
    prefix = 'Web2Cit/data/'
    prefix_monitor = 'Web2Cit/monitor'

    def __init__(self):
        self.site = pywikibot.Site('meta')
        self.generator = pagegenerators.PrefixingPageGenerator(
            self.prefix, site=self.site)

    def run(self) -> Set:
        domains = []
        for page in self.generator:
            title = page.title().replace(self.prefix, '')
            parts = title.split('/')[:-1]
            json_name = title.split('/')[-1]
            if json_name.find('patterns.json') != -1:
                continue
            parts.reverse()
            domain = '.'.join(parts)
            domains.append(domain)

        return set(domains)

    def create_pages_monitor(self) -> Iterable[Page]:
        domains = []
        for domain in self.run():
            dom = Domain(domain)
            domains.append('{}/{}/log'.format(self.prefix_monitor,
                                              dom.get_domain_to_meta()))
        return pagegenerators.PagesFromTitlesGenerator(domains)

    def check_changed(self, hours: int = 1) -> Set:
        """
        Check if the current page has changed in X hours
        """
        domains = []
        for page in self.generator:
            if ((page.editTime() + datetime.timedelta(hours=hours)) < datetime.datetime.now()):
                continue

            title = page.title().replace(self.prefix, '')
            parts = title.split('/')[:-1]
            parts.reverse()
            domain = '.'.join(parts)
            domains.append(domain)

        return set(domains)

    def check_update(self, days: int = 30) -> Set:
        """
        Check if the current page has changed in X days
        """
        pages = self.create_pages_monitor()
        pages = filter(lambda x: x.exists() is True, pages)
        domains = []

        for page in pages:
            if ((page.editTime() + datetime.timedelta(days=days)) > datetime.datetime.now()):
                continue
            title = page.title().replace(self.prefix_monitor+'/', '')
            parts = title.split('/')[:-1]
            parts.reverse()
            domain = '.'.join(parts)
            domains.append(domain)

        return set(domains)

    def check_new(self) -> Set:
        """
        Check if the domain has no results, so this is a new domain to write
        """
        pages = self.create_pages_monitor()
        pages = filter(lambda x: x.exists() is False, pages)
        domains = []

        for page in pages:
            title = page.title().replace(self.prefix_monitor+'/', '')
            parts = title.split('/')[:-1]
            parts.reverse()
            domain = '.'.join(parts)
            domains.append(domain)

        return set(domains)

    def check_monitor(self, edit: int = 1, update: int = 30) -> dict:
        """
        Check if the current page has changed in X hours
        """
        return {
            'edit': self.check_changed(edit),
            'update': self.check_update(update),
            'new': self.check_new()
        }
