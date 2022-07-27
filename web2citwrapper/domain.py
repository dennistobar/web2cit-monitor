from . import comm, Result


class URLParseError(Exception):
    pass


class Domain(object):
    def __init__(self, domain: str):
        self.domain = domain

    def retrieve(self) -> list:
        json = comm.get({'domain': self.domain, 'tests': 'true'})
        targets = self._parse_response(json)
        results = []
        for target in targets:
            results.append(Result(target))
        return results

    def _parse_response(self, json: dict = None) -> dict:
        if 'data' not in json.keys():
            raise URLParseError()
        if 'targets' not in json.get('data') or isinstance(json.get('data').get('targets'), list) == False:
            raise URLParseError()
        return json.get('data').get('targets')
