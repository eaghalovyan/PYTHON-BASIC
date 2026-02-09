"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    >>>is_http_domain('http://wikipedia.org')
    True
    >>>is_http_domain('https://ru.wikipedia.org/')
    True
    >>>is_http_domain('griddynamics.com')
    False
"""
import re


def is_http_domain(domain: str) -> bool:
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/?$'
    return  bool(re.fullmatch(pattern, domain))




"""
write tests for is_http_domain function
"""
import pytest

@pytest.mark.parametrize(
    "domain, result",
    [
       ('http://wikipedia.org', True),
       ('https://ru.wikipedia.org/', True),
       ('griddynamics.com', False), 
    ]
)
def test_is_http_domain(domain, result):
    assert is_http_domain(domain) == result