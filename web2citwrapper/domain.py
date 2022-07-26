from web2citwrapper import comm


class Domain(object):
    def __init__(self, domain):
        self.domain = domain

    def tests(self):
        return comm.get({'domain': self.domain, 'tests': 'true'})

    def score(self):
        tests = self.tests()
        scores = {}
        for test in tests:
            local_fields = test.get('results').pop().get('fields')
            scores[test.get('href')] = list(
                map(lambda x: x.get('score'), local_fields))

        return scores

    def __str__(self):
        return self.domain
