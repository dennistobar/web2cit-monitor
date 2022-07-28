from typing import Iterator
from . import comm, Result


class URLParseError(Exception):
    """Raised when the JSON cannot be parsed"""


class Domain(object):
    def __init__(self, domain: str):
        self.domain = domain

    def retrieve(self) -> Iterator[Result]:
        json = comm.get({'domain': self.domain, 'tests': 'true'})
        targets = self._parse_response(json)
        for target in targets:
            yield Result(target)

    def _parse_response(self, json: dict = None) -> dict:
        if 'data' not in json.keys():
            raise URLParseError
        if 'targets' not in json.get('data') or isinstance(json.get('data').get('targets'), list) is False:
            raise URLParseError
        return json.get('data').get('targets')
