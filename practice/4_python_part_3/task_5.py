"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
from urllib.request import urlopen


def make_request(url: str) -> Tuple[int, str]:
    with urlopen(url) as response:
        status = response.getcode()
        response_data = response.read().decode('utf-8')
        return status, response_data


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""


import pytest
from unittest.mock import MagicMock, patch

def test_make_request():
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'response data'
    mock_response.__enter__.return_value = mock_response

    with patch(__name__ + '.urlopen', return_value = mock_response) as mock_urlopen:
        status, data = make_request("https://example.com")

        assert status == 200
        assert data == 'response data'



# without patch
# import pytest
# from unittest.mock import MagicMock

# def test_make_request():
#     global urlopen
#     original_urlopen = urlopen
#     try:
#         mock_response = MagicMock()
#         mock_response.getcode.return_value = 200
#         mock_response.read.return_value = b'response data'

#         mock_response.__enter__.return_value = mock_response
#         mock_response.__exit__.return_value = None

#         mock_urlopen = MagicMock(return_value = mock_response)
#         urlopen = mock_urlopen
#         status, data = make_request("https://example.com")

#         assert status == 200
#         assert data == 'response data'

#     finally:
#         urlopen = original_urlopen

