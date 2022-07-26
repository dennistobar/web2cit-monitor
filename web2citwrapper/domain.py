from web2citwrapper import comm


class Domain(object):
    def __init__(self, domain):
        self.domain = domain

    def tests(self):
        return comm.get({'domain': self.domain, 'tests': 'true'})

    def score(self):
        tests = self.tests()

    def __str__(self):
        return self.domain
