from . import comm


class Page(object):
    def __init__(self, url=None):
        self.url = url

    def info(self):
        """Retrieve general information from page"""
        return comm.get({'url': self.url})

    def tests(self):
        """Run the tests about the URL"""
        return comm.get({'url': self.url, 'tests': 'true'})

    def score(self):
        """Retrieve score from a path testing"""
        tests = self.tests()
        scores = {}
        for test in tests:
            results = filter(lambda x: 'results' in x.keys(), tests)
            fields = map(lambda x: x['score'], list(
                results)[0].get('results')[0].get('fields'))
            scores[test['href']] = list(fields)

        return scores
