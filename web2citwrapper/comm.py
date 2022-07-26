import requests

URL = 'https://web2cit.toolforge.org/translate?'

PARAMETERS = {'format': 'json'}


class URLMissingError(Exception):
    pass


def get(parameters=None):
    """Retrieve a simple endpoint to web2cit"""
    if parameters is None:
        raise URLMissingError

    request = requests.get(URL, {**PARAMETERS, **parameters})
    return request.json()
