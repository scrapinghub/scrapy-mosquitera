import pytest
import six

from scrapy_mosquitera import PaginationMixin
from scrapy.http import Request
from scrapy.exceptions import DontCloseSpider

from pytest_bdd import when, then, given, scenarios, parsers
from tests.utils import given_response

converters = dict(
    n_requests=int
)
scenarios('./mixin.feature', example_converters=converters)

RESPONSE_ID = 'abcdef'


@given('an instance of the mixin')
def mixin_instance():
    return PaginationMixin()


@given('a response with id', target_fixture='response')
def a_response_with_id():
    response = given_response(
        url='http://domain.tld',
        meta={'__id': RESPONSE_ID}
    )

    return response


@given('a response with nprs inside', target_fixture='response')
def response_with_nprs_inside(response):
    meta = {
        'remaining_nprs': [Request(url='http://domain.tld')],
        'ocb': lambda v: {'item': 'yes'}
    }
    return given_response(url='http://domain.tld', meta=meta)


@when('request registry has counters > 0')
def request_registry_has_counters_greater_than_0(mixin_instance):
    mixin_instance._request_registry[RESPONSE_ID] = {'counter': 5}


@when('request registry has some counters = 0')
def request_registry_has_some_counters_equal_0(mixin_instance):
    mixin_instance._request_registry[RESPONSE_ID] = {
        'counter': 0,
        'nprs': [Request(url='http://domain.tld')]
    }


@when('I add an identifier to the request')
def add_an_identifier_to_the_request(req):
    req = PaginationMixin._add_identifiers_to_request(req, RESPONSE_ID)


@when('I use the response to increase the counter')
def use_the_response_to_increase_the_counter(mixin_instance, response):
    mixin_instance._increase_counter(response)


@when('I use the response to decrease the counter')
def use_the_response_to_decrease_the_counter(mixin_instance, response):
    mixin_instance._decrease_counter(response)


@when('I set the response for the pagination mixin')
def set_the_response_for_the_pagination_mixin(mixin_instance):
    mixin_instance.response_for_pagination_mixin = given_response(
        url='http://domain.tld',
        meta={'tag': 1, '__id': RESPONSE_ID}
    )


@when("there's some response id cache")
def theres_some_response_id_cache(mixin_instance):
    mixin_instance._response_id_cache = {'http://domain.tld': RESPONSE_ID}


@when("there's no response id cache")
def theres_no_response_id_cache(mixin_instance):
    mixin_instance._response_id_cache = {}


@when('I register requests with a method returning <n_requests>')
def register_requests_with_a_method_returning_n_requests(n_requests, mixin_instance):
    @mixin_instance.register_requests
    def generate_requests(self, number):
        r = []
        for i in range(number):
            r.append(Request(url='http://domain.tld/post%d' % i))

        return r

    mixin_instance._result = generate_requests(mixin_instance, n_requests)


@when('I deregister response')
def deregister_response(mixin_instance):
    @mixin_instance.deregister_response
    def generate_item(self):
        return {'test': 'yes'}

    generate_item(mixin_instance)


@when('I enqueue a method returning <n_requests>')
def enqueue_a_method_returning_n_requests(n_requests, mixin_instance):
    @mixin_instance.enqueue_next_page_requests
    def generate_requests(self, number):
        r = []
        for i in range(number):
            r.append(Request(url='http://domain.tld/post%d' % i))

        return r

    generate_requests(mixin_instance, n_requests)


@when('I mock crawler')
def mock_crawler(mocker, mixin_instance):
    mocker.patch.object(mixin_instance, 'crawler', create=True)


@then('many requests are yielded from call next page requests')
def many_requests_are_yielded_from_call_next_page_requests(mixin_instance, response):
    result = list(mixin_instance.call_next_page_requests(response))
    assert len(result) > 1


@then('the counter of nprs is <n_requests>')
def the_counter_of_nprs_is_n_requests(mixin_instance, n_requests):
    rid = mixin_instance.response_for_pagination_mixin.meta['__id']
    nprs = mixin_instance._request_registry[rid]['nprs']
    assert len(nprs) == n_requests


@then('it has initial attributes set')
def has_initial_attributes_set(mixin_instance):
    assert hasattr(mixin_instance, '_request_registry')
    assert hasattr(mixin_instance, '_response_id_cache')
    assert hasattr(mixin_instance, '_was_setup_called')


@then('every request is marked')
def every_request_is_marked(mixin_instance):
    for req in mixin_instance._result:
        assert req.meta['__id']


@then('the counter for the response is <n_requests>')
def the_counter_for_the_response_is_n_requests(n_requests, mixin_instance):
    rid = mixin_instance._get_response_id(
        mixin_instance.response_for_pagination_mixin
    )
    assert mixin_instance._request_registry[rid]['counter'] == n_requests


@then('the identifier is present in the request')
def the_identifier_is_present_in_the_request(req):
    assert req.meta['__id']


@then(parsers.parse('the counter for the response is {number:d}'))
def the_counter_for_the_response_is_number(mixin_instance, number):
    assert mixin_instance._request_registry[RESPONSE_ID]['counter'] == number


@then('getting response returns the same response')
def get_the_same_response_after_calling_get_response(mixin_instance):
    result = mixin_instance._get_response(None, None)
    assert result.meta['tag']


@then('getting response without response object raises exception')
def calling_get_response_without_response_object_raises_exception(mixin_instance):
    with pytest.raises(ValueError):
        mixin_instance._get_response([], {})


@then('getting response with any response objects returns the first one')
def calling_get_response_with_n_responses_gives_us_the_first_response(mixin_instance):
    responses = []
    for i in range(3):
        responses.append(given_response(meta={'tag': i}))

    result = mixin_instance._get_response((responses[:1]))
    assert result.meta['tag'] == 0

    result = mixin_instance._get_response((responses))
    assert result.meta['tag'] == 0


@then('I get the response id from the cache')
def get_the_response_id_from_the_cache(mixin_instance, response):
    assert mixin_instance._get_response_id(response) == RESPONSE_ID


@then('I get a new response id')
def get_a_new_response_id(mixin_instance, response):
    result = mixin_instance._get_response_id(response)
    assert isinstance(result, six.string_types)
    assert result != RESPONSE_ID


@then("at dequeuing it doesn't raise dont close spider")
def at_dequeuing_it_doesnt_raisee_dont_close_spider(mixin_instance):
    mixin_instance.dequeue_next_page_requests(None)


@then('at dequeuing it raises dont close spider')
def at_dequeuing_it_raises_dont_close_spider(mixin_instance):
    with pytest.raises(DontCloseSpider):
        mixin_instance.dequeue_next_page_requests(None)
