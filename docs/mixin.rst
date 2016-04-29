.. _mixin:

PaginationMixin
===============

:class:`PaginationMixin <.PaginationMixin>` is a mixin with a group of decorators
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


To understand better its working, please review the :ref:`examples <example_mixin>`.


.. autoclass:: scrapy_mosquitera.mixin.PaginationMixin
    :members: register_requests, deregister_response, enqueue_next_page_requests
