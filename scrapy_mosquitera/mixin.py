import uuid
import logging
import types

from collections import defaultdict
from functools import wraps

from scrapy import signals
from scrapy.http import Request, Response
from scrapy.exceptions import DontCloseSpider
from pydispatch import dispatcher
from pydispatch.errors import DispatcherKeyError


class PaginationMixin(object):
    def _set_attributes_to_initial_state(self):
        # Each entry in registry has {'counter': int, 'nprs': []}
        self._request_registry = defaultdict(dict)
        self._response_id_cache = {}

    def __init__(self, *args, **kwargs):
        super(PaginationMixin, self).__init__(*args, **kwargs)

        self._set_attributes_to_initial_state()
        self._was_setup_called = False

    def dm_setup(self):
        """ Set method for spider idle state.
        It's implemented this way to support one and many instances of the mixin.

        """
        dispatcher.connect(
            self.dequeue_next_page_requests,
            signal=signals.spider_idle
        )
        self._was_setup_called = True

    def dm_teardown(self):
        """ Disconnect the method from the signal.
        It's done to avoid conflicts when many instances of the mixin are being executed.

        """
        try:
            dispatcher.disconnect(
                self.dequeue_next_page_requests,
                signal=signals.spider_idle
            )
        except DispatcherKeyError:
            pass

    @staticmethod
    def _add_identifiers_to_request(request, response_id):
        """ Add ``response_id`` to ``request`` meta. """
        meta = request.meta
        meta['__id'] = response_id
        return request.replace(meta=meta)

    def _increase_counter(self, response):
        """ Increase registry counter for identifier inside ``response``. """
        response_id = response.meta['__id']
        spot = self._request_registry[response_id]
        spot['counter'] = spot.get('counter', 0) + 1

    def _decrease_counter(self, response):
        """ Decrease registry counter for identifier inside ``response``. """
        response_id = response.meta['__id']
        spot = self._request_registry[response_id]
        spot['counter'] = spot.get('counter', 0) - 1

    def _get_response(self, args=[], kwargs={}):
        """ Get response from ``args`` or ``kwargs``. """
        # If you're decorating a function without response objects as arguments
        # or invalid ones, you can set this attribute that has precedence.
        if hasattr(self, 'response_for_pagination_mixin'):
            return self.response_for_pagination_mixin

        total_args = list(args) + list(kwargs.values())
        response_objs = [obj for obj in total_args if isinstance(obj, Response)]
        n_response_objs = len(response_objs)

        if n_response_objs == 0:
            raise ValueError('No response could be extracted.')
        if n_response_objs == 1:
            return response_objs[0]
        elif n_response_objs > 1:
            logging.warning('[-] Detected more than one response. Using the first one.')
            return response_objs[0]

    def _get_response_id(self, response):
        """ Return response_id from cache or generate it.
            It's a short-term cache, just for the current batch of responses.

        """
        if response.url in self._response_id_cache:
            return self._response_id_cache[response.url]
        else:
            response_id = str(uuid.uuid4())
            self._response_id_cache[response.url] = response_id
            return response_id

    @staticmethod
    def register_requests(fn):
        """ Register requests yielded from ``fn`` in the registry
            using as key its parent response id.

            It's a decorator.

        """
        @wraps(fn)
        def inner(self, *args, **kwargs):
            if not self._was_setup_called:
                self.dm_setup()

            response = self._get_response(args, kwargs)
            response_id = self._get_response_id(response)
            response.meta['__id'] = response_id

            result = fn(self, *args, **kwargs)
            if not result:
                return

            # Save original type to return the same results from ``fn``
            original_type = type(result)

            if isinstance(result, Request):
                result = [result]

            request_list = []
            for r in result:
                if isinstance(r, Request):
                    r = self._add_identifiers_to_request(r, response_id)
                    self._increase_counter(response)

                request_list.append(r)

            if original_type in (list, types.GeneratorType):
                return request_list
            else:
                return request_list[0]

        return inner

    @staticmethod
    def deregister_response(fn):
        """ Deregister response from the registry.

        It's a decorator.

        """
        @wraps(fn)
        def inner(self, *args, **kwargs):
            item_or_request = fn(self, *args, **kwargs)

            # Only decrease counter if the item_or_request passed the filter
            if item_or_request:
                response = self._get_response(args, kwargs)
                self._decrease_counter(response)

            return item_or_request

        return inner

    @staticmethod
    def enqueue_next_page_requests(fn):
        """ Enqueue next page requests to be only requested if they meet the conditions.

        It's a decorator.

         """
        @wraps(fn)
        def inner(self, *args, **kwargs):
            logging.debug("[+] Queueing next page calls ..")
            request_or_requests = fn(self, *args, **kwargs)
            if not request_or_requests:
                return

            response = self._get_response(args, kwargs)
            response_id = response.meta['__id']

            # Transform to list if it's a single request
            if not isinstance(request_or_requests, list):
                request_or_requests = [request_or_requests]

            self._request_registry[response_id]['nprs'] = request_or_requests

        return inner

    def dequeue_next_page_requests(self, spider):
        """ Yield the first next page request meeting the conditions and
            recover spider from idle state.

        """
        logging.debug("[+] Dequeueing next page requests ..")
        valid_nprs = []

        for response_id, data in self._request_registry.items():
            if data['counter'] != 0:
                continue

            valid_nprs += data.get('nprs', [])

        # Get first next page request and save original callback
        try:
            npr = valid_nprs.pop(0)
        except IndexError:
            logging.info("[-] No more valid new page requests to process ..")
            return

        new_meta = npr.meta
        new_meta['ocb'] = npr.callback
        new_meta['remaining_nprs'] = valid_nprs
        new_npr = npr.replace(callback=self.call_next_page_requests, meta=new_meta)

        self.crawler.engine.schedule(new_npr, spider=spider)
        raise DontCloseSpider

    def call_next_page_requests(self, response):
        logging.debug("[+] Requesting next page requests ..")
        remaining_nprs = response.meta['remaining_nprs'][:]

        # Do some cleaning
        self._set_attributes_to_initial_state()
        self.dm_teardown()
        del response.meta['remaining_nprs']

        # Deal with current response
        # As they are pages parsing lists, they usually yield requests
        cb = response.meta['ocb']
        for request in cb(response):
            yield request

        # Yield pending next page requests
        for request in remaining_nprs:
            yield request
