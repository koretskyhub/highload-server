import os
import re
import string

__all__ = (
    'Request'
)

_REQUEST_LINE_RE = r'^(?P<method>[A-Z]+)\s+' \
                   r'((?P<scheme>http[s]?)://)?' \
                   r'(?P<host>[\w*\.]*\w+)?/?' \
                   r'(?P<path>[^\?]*)?(\?[^.]*)?(\#.*)?\s+' \
                   r'(?P<http_ver>HTTP/1.[1|0])$'

class Request():
    _DELIMITER = '\r\n'
    _EMPTY_STRING = '\r\n' * 2
    _INDEX_FILE = 'index.html'
    _REQUEST_LINE_PATTERN = re.compile(_REQUEST_LINE_RE)

    def __init__(self):
        self.method = None
        self.path = None
        self.headers = dict()


    def parse(self, raw_request):
        print(raw_request)
        if not raw_request or type(raw_request) != str:
            return False
        
        if raw_request.find(self._EMPTY_STRING) > 0:
            request, _ = raw_request.split(self._EMPTY_STRING)
        else:
            request = raw_request
        
        print(request)

        if request.find(self._DELIMITER) > 0:
            request_line, headers = request.split(self._DELIMITER, maxsplit=1)
            return self._parse_headers(headers) and self._parse_request_line(request_line)
        else:
            request_line = request
            return self._parse_request_line(request_line)



    def _parse_headers(self, raw_headers):
        if not raw_headers or type(raw_headers) != str:
            return False
        
        headers_list = raw_headers.split(self._DELIMITER)

        for header in headers_list:
            key, value = list(map(lambda x: x.strip(), header.split(':', maxsplit=1)))
            self.headers[key] = value

        return True


    def _parse_request_line(self, raw_request_line):
        if not raw_request_line or type(raw_request_line) != str:
            return False

        match = self._REQUEST_LINE_PATTERN.search(raw_request_line)

        if not match:
            print('request_line not matching regexp')
            return False

        self.method = match.group('method')

        self.path = match.group('path')

        #если путь ведет в родительские каталоги
        if self.path.find('/../') > 0:
            return False

        return True


if __name__ == '__main__':
    request_str = 'GET / HTTP/1.1\r\n' \
                  'User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)\r\n'\
                  'Host : www.tutorialspoint.com\r\n'\
                  'Accept-Language: en-us\r\n'\
                  'Accept-Encoding: gzip, deflate\r\n'\
                  'Connection: Keep-Alive\r\n\r\n'\
                  'body'
    r = Request()
    r.parse(request_str)
