import datetime
import dateparser

from pytest_bdd import then, given, scenarios
from scrapy_mosquitera.matchers.date import (
    _to_datetime, has_valid_date, _get_min_date, _get_max_date,
    date_matches, date_in_period_matches, _date_in_period_day,
    _date_in_period_week, _date_in_period_month, _date_in_period_year
)


converters = dict(
    n_requests=int,
    target_date=dateparser.parse,
    min_date=dateparser.parse,
    max_date=dateparser.parse,
    true_or_false=eval,
    maximum=eval
)
scenarios('./date.feature', example_converters=converters)


@given('a datetime object')
def datetime_obj():
    return datetime.datetime.utcnow()


@given('a string with date format')
def date_string():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d')


@given('a date object')
def date_obj():
    return datetime.date.today()


@given('a invalid date string')
def invalid_date_string():
    return '---'


@given('target date <target_date>')
def target_date(target_date):
    return target_date


@given('min date <min_date>')
def min_date(min_date):
    return min_date


@given('max date <max_date>')
def max_date(max_date):
    return max_date


@given('a parameter <param> with value the datetime object')
def param_dict(datetime_obj, param):
    return {param: datetime_obj}


@given('empty data')
def data():
    return None


@then('transforming datetime to datetime returns the same object')
def transforming_datetime_to_datetime_returns_the_same_object(datetime_obj):
    rs = _to_datetime(datetime_obj)
    assert rs == datetime_obj


@then('transforming date string to datetime returns a valid datetime object')
def transforming_date_string_to_datetime_returns_a_valid_datetime_object(date_string):
    rs = _to_datetime(date_string)
    assert isinstance(rs, datetime.datetime)


@then('transforming date object to datetime returns a valid datetime object')
def transforming_date_object_to_datetime_returns_a_valid_datetime_object(date_obj):
    rs = _to_datetime(date_obj)
    assert isinstance(rs, datetime.datetime)


@then('transforming an invalid date string raises exception')
def transforming_an_invalid_date_string_raises_exception(invalid_date_string):
    try:
        _to_datetime(invalid_date_string)
        assert False
    except TypeError:
        assert True


@then('has valid date is <true_or_false>')
def has_valid_date_is(true_or_false, target_date, min_date, max_date):
    assert has_valid_date(target_date, min_date, max_date) == true_or_false


@then('minimum date equal to datetime object is <true_or_false>')
def minimum_date_equal_to_datetime_object_is_(true_or_false, param_dict, datetime_obj):
    rs = _get_min_date(param_dict) == datetime_obj
    assert rs == true_or_false


@then('maximum date equal to datetime object is <true_or_false>')
def maximum_date_equal_to_datetime_object_is_(true_or_false, param_dict, datetime_obj):
    rs = _get_max_date(param_dict) == datetime_obj
    assert rs == true_or_false


@then('minimum date is the default')
def minimum_date_is_the_default(param_dict):
    rs = _get_min_date(param_dict)
    assert isinstance(rs, datetime.datetime)
    assert rs == datetime.datetime.min


@then('maximum date is the default')
def maximum_date_is_the_default(param_dict):
    rs = _get_max_date(param_dict)
    assert isinstance(rs, datetime.datetime)
    assert rs == datetime.datetime.max


@then('date matches is <true_or_false>')
def date_matches_is(true_or_false, data):
    assert date_matches(data) == true_or_false


@then('date in period matches is <true_or_false>')
def date_in_period_matches_is(true_or_false, data):
    assert date_in_period_matches(data) == true_or_false


@then('date in period day with <maximum> is <true_or_false>')
def date_in_period_day_with_maximum_is(maximum, true_or_false, target_date, min_date, max_date):
    assert _date_in_period_day(target_date, min_date, max_date, maximum) == true_or_false


@then('date in period week with <maximum> is <true_or_false>')
def date_in_period_week_with_maximum_is(maximum, true_or_false, target_date, min_date, max_date):
    assert _date_in_period_week(target_date, min_date, max_date, maximum) == true_or_false


@then('date in period month with <maximum> is <true_or_false>')
def date_in_period_month_with_maximum_is(maximum, true_or_false, target_date, min_date, max_date):
    assert _date_in_period_month(target_date, min_date, max_date, maximum) == true_or_false


@then('date in period year with <maximum> is <true_or_false>')
def date_in_period_year_with_maximum_is(maximum, true_or_false, target_date, min_date, max_date):
    assert _date_in_period_year(target_date, min_date, max_date, maximum) == true_or_false
