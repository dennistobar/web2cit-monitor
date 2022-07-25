import requests

URL = 'https://web2cit.toolforge.org/translate'

PARAMETERS = {'format': 'json'}


def get(url, parameters=None):
    """Retrieve a simple endpoint to web2cit"""
    if parameters is None:
        parameters = PARAMETERS

    url = URL + '?url={}'.format(url)

    request = requests.get(url, {**PARAMETERS, **parameters})
    return request.json()
