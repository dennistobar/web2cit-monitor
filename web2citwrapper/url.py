from . import comm


class URL(object):
    def __init__(self, url=None):
        self.url = url

    def info(self):
        return comm.get({'url': self.url})

    def tests(self):
        return comm.get({'url': self.url, 'tests': 'true'})
