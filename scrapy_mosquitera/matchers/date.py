import datetime

import dateparser
import six


def get_week_number_from_date(date_obj):
    return date_obj.isocalendar()[1]


def _to_datetime(v):
    """ Return datetime object or raise TypeError after parsing ``v``. """
    if isinstance(v, datetime.datetime):
        return v

    if isinstance(v, six.string_types):
        return dateparser.parse(v)

    if isinstance(v, datetime.date):
        return datetime.datetime.combine(v, datetime.datetime.min.time())

    raise TypeError('Invalid argument for date type.')


def has_valid_date(target_date, min_date, max_date):
    """ Return ``True`` if ``target_date`` is inside the range [min_date, max_date] """
    return min_date <= target_date < max_date


def _get_min_date(kwargs):
    """ Return datetime object or None. """
    min_date = datetime.datetime.min
    on = kwargs.get('on')
    after = kwargs.get('after')
    since = kwargs.get('since')
    min_date_arg = kwargs.get('min_date')

    if min_date_arg:
        min_date = _to_datetime(min_date_arg)
    elif on:
        min_date = _to_datetime(on)
    elif after:
        min_date = _to_datetime(after)
    elif since:
        min_date = _to_datetime(since)

    return min_date


def _get_max_date(kwargs):
    """ Return datetime object or None.

    Time in result is set to 23:59 if no time is provided.

    """
    max_date = datetime.datetime.max
    on = kwargs.get('on')
    before = kwargs.get('before')
    max_date_arg = kwargs.get('max_date')

    if max_date_arg:
        max_date = _to_datetime(max_date_arg)
    elif on:
        max_date = _to_datetime(on)
    elif before:
        max_date = _to_datetime(before)

    # Set to midnight if time is not set
    if max_date and not (max_date.hour or max_date.minute or max_date.second):
        max_date = max_date.replace(hour=23, minute=59, second=59)

    return max_date


def date_matches(data, **kwargs):
    """ Return ``True`` or ``False`` if ``data`` has a valid date.

    Arguments in kwargs:

    * on : min date is date at 00:00 and max date is date at 23:59
    * since or after: sets min date
    * before: sets max date, at 23:59 if no time is provided

    ``data`` and ``kwargs`` arguments can use any valid datetime object or
    more human-readable sentences like '3 days ago' as far as dateparser supports it.

    """
    if not data:
        return False

    target_date = _to_datetime(data)
    min_date = _get_min_date(kwargs)
    max_date = _get_max_date(kwargs)

    return has_valid_date(target_date, min_date, max_date)


def date_in_period_matches(data, period='day', check_maximum=True, **kwargs):
    """ Return ``True`` if ``data`` is in the valid date range defined by ``period``.

    """
    if not data:
        return False

    target_date = _to_datetime(data)
    min_date = _get_min_date(kwargs)
    max_date = _get_max_date(kwargs)

    # jettison tzinfo to force comparison only with naive approach
    target_date = target_date.replace(tzinfo=None)

    if period == 'day':
        result = min_date <= target_date

        if result and check_maximum:
            result &= target_date < max_date

    elif period in ['week', 'weeks']:
        week_under_question = target_date.year, get_week_number_from_date(target_date)
        min_week = min_date.year, get_week_number_from_date(min_date)
        result = min_week <= week_under_question

        if result and check_maximum:
            max_week = max_date.year, get_week_number_from_date(max_date)
            result &= week_under_question <= max_week

    elif period in ['month', 'months']:
        month_under_question = target_date.year, target_date.month
        min_month = min_date.year, min_date.month
        result = min_month <= month_under_question

        if result and check_maximum:
            max_month = max_date.year, max_date.month
            result &= month_under_question <= max_month

    elif period in ['year', 'years']:
        result = min_date.year <= target_date.year

        if result and check_maximum:
            result &= target_date.year <= max_date.year

    else:
        raise ValueError('Unknown period: {period}'.format(period=period))

    return result
