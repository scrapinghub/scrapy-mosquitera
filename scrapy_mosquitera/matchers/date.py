import datetime

import dateparser
import six


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
    result = True

    if min_date:
        result = min_date <= target_date

    if result and max_date:
        result &= target_date < max_date

    return result


def _get_min_date(kwargs):
    """ Return datetime object or None. """
    min_date = None
    on = kwargs.get('on')
    after = kwargs.get('after')
    since = kwargs.get('since')

    if on:
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
    max_date = None
    on = kwargs.get('on')
    before = kwargs.get('before')

    if on:
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
