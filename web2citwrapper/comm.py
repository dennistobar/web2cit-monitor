import requests

URL = 'https://web2cit.toolforge.org/translate'

PARAMETERS = {'format': 'json'}


def get(url, parameters={}):
    """Retrieve a simple endpoint to web2cit"""
    url = URL + '?url={}'.format(url)

    request = requests.get(url, {**PARAMETERS, **parameters})
    return request.json()
