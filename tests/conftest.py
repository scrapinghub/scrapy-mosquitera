from scrapy.http import Request
from pytest_bdd import given
from tests.utils import given_response


@given('a response')
def response():
    return given_response(url='http://domain.tld/post1')


@given('a request')
def req():
    return Request(url='http://domain.tld')
