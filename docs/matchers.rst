.. _matchers:

Matchers
========

Creating your own matcher
^^^^^^^^^^^^^^^^^^^^^^^^^

A matcher is a simple function taking the data to be evaluated as argument(s)
and returning a boolean value according to its validity.


Current matchers
----------------

Date Matchers
^^^^^^^^^^^^^

The date matchers use a lot of words to delimit their date range.
They are separated to set the maximum and minimum date.
In order of precedence they are for minimum date:

* min_date
* on
* after
* since

And for maximum date:

* max_date
* on
* before

Their values could be dates parseables by `dateparser`_, ``date`` or ``datetime`` objects.
They also support ``None`` value, so that limit isn't verified.


.. automodule:: scrapy_mosquitera.matchers
    :members: date_matches, date_in_period_matches

.. _dateparser: https://github.com/scrapinghub/dateparser
