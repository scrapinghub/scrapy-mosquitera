.. scrapy-mosquitera documentation master file, created by
   sphinx-quickstart on Fri Apr 15 18:25:09 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to scrapy-mosquitera's documentation!
=============================================


.. epigraph::

   How can I scrape items from a site from the last five days?

   -- Scrapy User



That question started the development of **scrapy-mosquitera**,
a project that restricts crawl and scraping scope using matchers.
A matcher is a simple function that returns
the validity of an element under certain restrictions.
The first goal in the project was date matching
but you will see it's easy to create any kind of matcher.


* :ref:`Matchers <matchers>`
* :ref:`Examples with date matcher and PaginationMixin <examples>`
