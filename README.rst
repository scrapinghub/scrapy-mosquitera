===============================================
scrapy-mosquitera - tools for filtered scraping
===============================================


.. image:: https://travis-ci.org/scrapinghub/scrapy-mosquitera.svg?branch=master
        :target: https://travis-ci.org/scrapinghub/scrapy-mosquitera


.. epigraph::

   How can I scrape items off a site from the last five days?

   -- Scrapy User


That question started the development of **scrapy-mosquitera**, a tool to help
you restrict crawling and scraping scope using *matchers*.

Matchers are simple Python functions that return the validity of an element
under certain restrictions.

The first goal in the project was date matching, but you can create your own
matcher for your own crawling and scraping needs.


How it works
============

In the case where the dates are available in the URLs, you will just use
the matcher function directly in your code::


  from scrapy_mosquitera.matchers import date_matches

   date = scrape_date_from_url(url)

   if date_matches(data=date, after='5 days ago'):
      yield Request(url=url, callback=self.parse_item)


To handle the case when the date is only available at the time when you scrape
the items, **scrapy-mosquitera** provides a ``PaginationMixin`` to control the
crawl according to the dates scraped.

Head on to the remaining of the `documentation`_  for more details.

.. _documentation: http://scrapy-mosquitera.readthedocs.io
