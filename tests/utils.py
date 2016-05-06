from scrapy.http import Response, Request, HtmlResponse, XmlResponse


class HtmlResponseWithMeta(HtmlResponse, Response):
    pass


class XmlResponseWithMeta(XmlResponse, Response):
    pass


def given_response(url='http://domain/path/', body='', meta={}, status=200, dtype='html'):
    # Trick to pass meta to response
    r = Request(url=url, meta=meta)
    if dtype == 'html':
        response_class = HtmlResponseWithMeta
    elif dtype == 'xml':
        response_class = XmlResponseWithMeta

    return response_class(url, body=body, request=r, status=status, encoding='ascii')
