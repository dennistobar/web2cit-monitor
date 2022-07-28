from web2citwrapper import comm
from typing import Iterator


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
        if 'results' not in self.data.keys():
            raise NoResultsError
        if isinstance(self.data.get('results'), list) is False:
            raise NoResultsError
        if len(self.data.get('results')) == 0:
            raise NoResultsError
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

    def __init__(self, value: dict = None):
        self.value = value

    def retrieve(self) -> Iterator[ResultElement]:
        """Obtain elements from communication with API"""
        json = comm.get({**self.value, 'tests': 'true'})
        targets = self._parse_response(json)
        for target in targets:
            yield ResultElement(target)

    def _parse_response(self, json: dict = None) -> dict:
        """Parse the JSON retrieved"""
        if 'data' not in json.keys():
            raise NoResultsError
        if 'targets' not in json.get('data'):
            raise NoResultsError
        if isinstance(json.get('data').get('targets'), list) is False:
            raise NoResultsError
        if len(json.get('data').get('targets')) == 0:
            raise NoResultsError
        return json.get('data').get('targets')


class Domain(ElementBase):
    def __init__(self, domain: str):
        super().__init__({'domain': domain})


class URL(ElementBase):
    def __init__(self, url: str = None):
        super().__init__({'url': url})

    def retrieve(self) -> ResultElement:
        return next(super().retrieve())
