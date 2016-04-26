.. _examples:

Examples
========

**scrapy-mosquitera** aims scenarios where there are listings involved.
However, **scrapy-mosquitera** takes a different approach whether the data to match
is present in the listing or not.
As it started for date validation,
let's review what to do when dates are present or absent.

Dates present
-------------

In example, we'll consider a blog archive page.

.. code-block:: html

  <div>
    <h3>Title for Post 1</h3>
    <a href="/post1">Link</a>
    <span>Posted on 2016-04-01</span>
  </div>
  <div>
    <h3>Title for Post 2</h3>
    <a href="/post2">Link</a>
    <span>Posted on 2016-04-02</span>
  </div>
  <div>
    <h3>Title for Post 3</h3>
    <a href="/post3">Link</a>
    <span>Posted on 2016-04-03</span>
  </div>


It's the simpler case since we can do the matching
at the method parsing the listing.

.. code-block:: python

  from scrapy_mosquitera.matchers import date_matches

  def parse(self, response):
    continue_to_next_page = True

    for news in response.xpath("//div"):
      date = news.xpath("./span/text()").re_first('Posted on (.*)')
      path_url = news.xpath("./a/@href").extract_first()
      url = response.urljoin(path_url)

      if date_matches(data=date, after='5 days ago'):
        yield Request(url=url, callback=self.parse_item)
      else:
        continue_to_next_page = False

    if continue_to_next_page:
      yield self.call_next_page(response)

The ``date_matches`` function is powered by `dateparser`,
so it can support written dates and datetime objects too.
The matcher let us control the pagination in an easy way.


Dates absent
------------

For this case, we'll consider the following blog archive page layout.

.. code-block:: html

  <div>
    <h3>Title for Post 1</h3>
    <a href="/post1">Link</a>
  </div>
  <div>
    <h3>Title for Post 2</h3>
    <a href="/post2">Link</a>
  </div>
  <div>
    <h3>Title for Post 3</h3>
    <a href="/post3">Link</a>
  </div>


Dates aren't present on the listing, but they are in each post page.

.. code-block:: html

  <h1>Title for Post</h1>
  <div>Posted on 2016-04-02</div>
  [...]


Here comes ``PaginationMixin``, which is a mixin with a group of decorators
to control the logic of requesting the next page.
It has an interesting flow, which could be summarized as:

   1. At the listing parsing method, every item page request is yielded.
      Each request is marked to be associated with the current response
      and any pagination requests is enqueued.
   2. At the item parsing method, the matching logic is applied and
      each valid item and its related request is registered.
   3. After comparing the yielded requests at step 1 and the requests
      which yielded valid items at step 2, the mixin decides
      to dequeue the next page request only if every request yielded a valid item.

So to see it in action in a comparable way with the first example,
let's start using their decorators.
``@PaginationMixin.register_requests`` has to be applied
to the listing parsing method.

.. code-block:: python

  from scrapy_mosquitera.matchers import PaginationMixin

  @PaginationMixin.register_requests
  def parse(self, response):
    for news in response.xpath("//div"):
      path_url = news.xpath("./a/@href").extract_first()
      url = response.urljoin(path_url)

      yield Request(url=url, callback=self.parse_item)

    yield self.call_next_page(response)

Unfortunately, each time that the listing parsing method is called
every item request will be made since we don't know yet
if its content is valid or not.
The method in charge of returning the next page request,
in this case ``call_next_page``,
has to be decorated with ``@PaginationMixin.enqueue_next_page_requests``.

.. code-block:: python

  @PaginationMixin.enqueue_next_page_requests
  def call_next_page(self, response):
    return Request([...])


This decorator saves the request to be called only if it's necessary.
Then, the last decorator has to be applied on the method parsing the item
since it has to register if a valid item was returned.
This decorator is ``@PaginationMixin.deregister_response``.

.. code-block:: python

  @PaginationMixin.deregister_response
  def parse_item(self, response):
    date = response.xpath("//div/text").re_first('Posted on (.*)')
    item = {'created_at': date}

    if date_matches(data=item['created_at'], after='5 days ago'):
      return item


After that, we're ready to run our spider.
First, it will make three requests, one for each post page and the pagination request will be saved.
Then, if the three post are valid, they will be scraped and the next page request will be made.
Otherwise, it only scrape the valid posts and the spider run will finish.
