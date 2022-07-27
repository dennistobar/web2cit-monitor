class ResultsNotFoundError(Exception):
    pass


class Result(object):
    data = {}

    def __init__(self, data: dict = None):
        self.data = data

    def path(self) -> str:
        """Obtain tested path"""
        return self.data.get('path')

    def result(self) -> dict:
        """Obtain results. Per design, results is an array with one element... it could be safe do .pop"""
        if 'results' not in self.data.keys():
            raise ResultsNotFoundError
        if not isinstance(self.data.get('results'), list) or len(self.data.get('results')) == 0:
            raise ResultsNotFoundError
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
