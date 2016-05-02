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
        dd = dateparser.parse(v)
        if dd:
            return dd

    if isinstance(v, datetime.date):
        return datetime.datetime.combine(v, datetime.datetime.min.time())

    raise TypeError('Invalid argument for date type.')


def has_valid_date(target_date, min_date, max_date):
    """ Return ``True`` if ``target_date`` is inside the range [min_date, max_date] """
    return min_date <= target_date < max_date


def _get_min_date(kwargs):
    """ Return datetime object or None.

    Accepted parameters:

    * min_date
    * on
    * after
    * since

    """
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

    Accepted parameters:

    * max_date
    * on
    * before

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
    """ Return ``True`` if ``data`` is a date in the valid date range.
    Otherwise ``False``.

    :param data: the date to validate
    :type data: string, date or datetime
    :param kwargs: special delimitation parameters
    :type kwargs: dict
    :rtype: bool

    """
    if not data:
        return False

    target_date = _to_datetime(data)
    min_date = _get_min_date(kwargs)
    max_date = _get_max_date(kwargs)

    return has_valid_date(target_date, min_date, max_date)


def _date_in_period_day(target_date, min_date, max_date, check_maximum):
    result = min_date <= target_date

    if result and check_maximum:
        result &= target_date < max_date

    return result


def _date_in_period_week(target_date, min_date, max_date, check_maximum):
    week_under_question = target_date.year, get_week_number_from_date(target_date)
    min_week = min_date.year, get_week_number_from_date(min_date)
    result = min_week <= week_under_question

    if result and check_maximum:
        max_week = max_date.year, get_week_number_from_date(max_date)
        result &= week_under_question <= max_week

    return result


def _date_in_period_month(target_date, min_date, max_date, check_maximum):
    month_under_question = target_date.year, target_date.month
    min_month = min_date.year, min_date.month
    result = min_month <= month_under_question

    if result and check_maximum:
        max_month = max_date.year, max_date.month
        result &= month_under_question <= max_month

    return result


def _date_in_period_year(target_date, min_date, max_date, check_maximum):
    result = min_date.year <= target_date.year

    if result and check_maximum:
        result &= target_date.year <= max_date.year

    return result


def date_in_period_matches(data, period='day', check_maximum=True, **kwargs):
    """ Return ``True`` if ``data`` is a date in the valid date range defined by ``period``.
        Otherwise ``False``.

        This matcher is ideal for cases like the following one.

        A forum post is created at *04-10-2016*. Then on *04-28-2016*,
        I try to scrape the forum covering the last few days.
        However, the forum doesn't display the post date but some sentences like *X weeks ago*.
        So, in the forum nomenclature, the posts fall in the next table:

        +------------+------------+-----------------+
        | Start date | End date   | Name            |
        +============+============+=================+
        | 04-15-2016 | 04-21-2016 | One week ago    |
        +------------+------------+-----------------+
        | 04-08-2016 | 04-14-2016 | Two weeks ago   |
        +------------+------------+-----------------+
        | 04-01-2016 | 04-07-2016 | Three weeks ago |
        +------------+------------+-----------------+

        On *04-28-2016*, if I calculate *two weeks ago* it will return *04-14-2016*.
        Comparing it to the forum meaning, we're working with fixed dates and
        the forum with date ranges.
        Then, if I scrape until *04-10-2016*, the crawl will miss the posts
        from *04-10-2016* to *04-13-2016* since the last valid date would be *two weeks ago*
        (*three weeks ago* is out of scope (*04-07-2016* < *04-10-2016*)).

        This matcher comes to solve this, so you can provide the period (in this case **week**)
        and you won't miss items by coverage issues.
        However, it's inclusive because to satisfy the date *04-10-2016* it will include the full week
        [04-08-2016, 04-14-2016], so a post-filtering should be made to only allow valid items.

        :param data: the date to validate
        :type data: string, date or datetime
        :param period: the period to evaluate ('day', 'month', 'year')
        :type period: string
        :param check_maximum: check maximum date
        :type check_maximum: bool
        :param kwargs: special delimitation parameters
        :type kwargs: dict
        :rtype: bool

    """
    if not data:
        return False

    target_date = _to_datetime(data)
    min_date = _get_min_date(kwargs)
    max_date = _get_max_date(kwargs)

    # jettison tzinfo to force comparison only with naive approach
    target_date = target_date.replace(tzinfo=None)

    if period == 'day':
        result = _date_in_period_day(target_date, min_date, max_date, check_maximum)
    elif period in ['week', 'weeks']:
        result = _date_in_period_week(target_date, min_date, max_date, check_maximum)
    elif period in ['month', 'months']:
        result = _date_in_period_month(target_date, min_date, max_date, check_maximum)
    elif period in ['year', 'years']:
        result = _date_in_period_year(target_date, min_date, max_date, check_maximum)
    else:
        raise ValueError('Unknown period: {period}'.format(period=period))

    return result
