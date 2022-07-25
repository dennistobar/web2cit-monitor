from . import comm


class Page(object):
    def __init__(self, url=None):
        self.url = url

    def info(self):
        """Retrieve general information from page"""
        return comm.get(self.url)

    def tests(self):
        """Run the tests about the URL"""
        return comm.get(self.url, {'tests': 'true'})

    def score(self):
        """Retrieve score from a path testing"""
        tests = self.tests()
        scores = {}
        print(scores)
        for test in tests:
            results = [test if 'results' in test.keys() else None]
            results = filter(lambda x: x != None, results)
            scores[test['path']] = list(map(lambda x: x.score, results))

        return scores
