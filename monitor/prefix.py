import datetime
from typing import Set
import pywikibot
from pywikibot import pagegenerators


class Prefix(object):
    prefix = 'Web2Cit/data/'

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

    def check_changed(self, hours: int = 1) -> Set:
        """
        Check if the current page has changed in X hours
        """
        domains = []
        for page in self.generator:
            delta = page.editTime() - datetime.datetime.now()
            if (delta < datetime.timedelta(hours=hours)):
                continue

            title = page.title().replace(self.prefix, '')
            parts = title.split('/')[:-1]
            parts.reverse()
            domain = '.'.join(parts)
            domains.append(domain)

        return set(domains)
