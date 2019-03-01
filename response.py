from datetime import datetime

__all__ = (
    'Response'
)

_HTTP_STATUS_MESSAGES = {
    200 : 'OK',
    403 : 'Forbidden',
    404 : 'Not Found',
    405 : 'Method Not Allowed',
}

class Response:
    HTTP_VERSION = '1.1'
    _SERVER_NAME = 'asyncio_prefork'
    _DELIMITER = '\r\n'
    
    def __init__(self, status_code, headers_dict={}):
        self.status_code = status_code
        self.headers_dict = headers_dict

    def _default_headers(self):
        return {
            'Connection': 'close',
            'Date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'Server': self._SERVER_NAME
        }

    def build_headers(self, headers_dict):
        headers_dict = {**headers_dict, **self._default_headers()}
        return self._DELIMITER.join(
            "{!s}: {!s}".format(key, val) for (key, val) in headers_dict.items()
            )


    def build_response_line(self, status):
        message = _HTTP_STATUS_MESSAGES.get(status) or ''
        return 'HTTP/{} {} {}'.format(self.HTTP_VERSION, status, message)


    def __str__(self):
        response_line = self.build_response_line(self.status_code)
        headers = self.build_headers(self.headers_dict)
        return r'{}{}{}{}'.format(response_line, self._DELIMITER, headers, self._DELIMITER * 2)


if __name__ == '__main__':
    d = {
        'Host' : 'www.tutorialspoint.com',
        'Accept-Language': 'en-us'
    }
    r = Response(200, d)
    print(str(r))