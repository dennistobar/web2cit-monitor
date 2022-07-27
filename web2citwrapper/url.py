from web2citwrapper.result import Result
from . import comm


class URLParseError(Exception):
    """Raised when the JSON can't be parsed"""
    pass


class URL(object):
    def __init__(self, url: str = None):
        self.url = url

    def retrieve(self) -> Result:
        json = comm.get({'url': self.url, 'tests': 'true'})
        data = self._parse_response(json)
        return Result(data)

    def _parse_response(self, json: dict = None) -> dict:
        if 'data' not in json.keys():
            raise URLParseError()
        if 'targets' not in json.get('data') or isinstance(json.get('data').get('targets'), list) == False:
            raise URLParseError()
        return json.get('data').get('targets')[0]
