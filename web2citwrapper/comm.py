import requests

URL = 'https://web2cit.toolforge.org/translate?'

PARAMETERS = {'format': 'json'}


class ParametersMissinError(Exception):
    """Raised when parameters is not provided"""


class Web2CitError(Exception):
    """Raised when the web2cit service returns an error"""


def get(parameters: dict = None) -> dict:
    """Retrieve a simple endpoint to web2cit"""
    if parameters is None:
        raise ParametersMissinError

    request = requests.get(URL, {**PARAMETERS, **parameters})
    json = request.json()
    if 'error' in json.keys():
        raise Web2CitError(json['error']['message'])

    return json
