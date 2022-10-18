from web2citwrapper import comm
from typing import Iterator
import statistics


class NoResultsError(Exception):
    """Raised the parsed element has no targets"""


class ResultElement(object):
    data = {}

    def __init__(self, data: dict = None):
        self.data = data

    def path(self) -> str:
        """Obtain tested path"""
        return self.data.get('path')

    def result(self) -> dict:
        """
        Obtain results. Per design, results is an array with one element...
        it could be safe do .pop
        """
        if 'error' in self.data.keys():
            raise NoResultsError(self.data.get('error').get('message', ''))
        if 'results' not in self.data.keys():
            raise NoResultsError('There is no results key')
        if isinstance(self.data.get('results'), list) is False:
            raise NoResultsError('results is not a list')
        if len(self.data.get('results')) == 0:
            raise NoResultsError('results has no elements')
        return self.data.get('results')[0]

    def fields(self) -> list:
        """Obtain all fields from result"""
        return self.result().get('fields')

    def score(self) -> float:
        """Obtain score of result"""
        return self.result().get('score')

    def href(self) -> str:
        """Obtain href for result"""
        return self.data.get('href')


class ElementBase(object):
    value = {}
    targets = []
    info_data = {}

    def __init__(self, value: dict = None):
        self.value = value

    def retrieve(self) -> Iterator[ResultElement]:
        """Obtain elements from communication with API"""
        if len(self.targets) == 0:
            json = comm.get({**self.value, 'tests': 'true'})
            self.info_data = json.get('info', {})
            self.targets = self._parse_response(json).get('targets')
            self.score_data = self._parse_response(json).get('score', 'n/d')
        for target in self.targets:
            yield ResultElement(target)

    def tests_counted(self) -> int:
        """Obtain number of tests"""
        return len(list(self.retrieve()))

    def score(self):
        """Obtain score of result"""
        return self.score_data

    def info(self) -> dict:
        """Obtain information about result"""
        if len(self.info_data) == 0:
            self.retrieve()
        return self.info_data

    def get_config(self, name: str) -> dict:
        """Obtain configuration for result"""
        if len(self.info_data) == 0:
            return None
        return self.info_data.get('config', {}).get(name, {}).get('revid', '-')

    def _parse_response(self, json: dict = None) -> dict:
        """Parse the JSON retrieved"""
        if 'error' in json.keys():
            raise NoResultsError(json.get('error').get('message', ''))
        if 'data' not in json.keys():
            raise NoResultsError('There is no "data" key')
        if 'targets' not in json.get('data'):
            raise NoResultsError('There is no "targets" key')
        if isinstance(json.get('data').get('targets'), list) is False:
            raise NoResultsError('Targets is not a list')
        if len(json.get('data').get('targets')) == 0:
            raise NoResultsError('Target is a empty list')
        return json.get('data')


class Domain(ElementBase):
    def __init__(self, domain: str):
        super().__init__({'domain': domain})

    def get_domain_to_meta(self):
        """Get the URL for the domain to use in Meta"""
        domain = self.value.get('domain')
        if domain is None:
            raise NoResultsError('Domain is not a valid domain')

        return "/".join(domain.split('.')[::-1])


class URL(ElementBase):
    def __init__(self, url: str = None):
        super().__init__({'url': url})

    def retrieve(self) -> ResultElement:
        return next(super().retrieve())
