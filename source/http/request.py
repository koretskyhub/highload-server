import os
import re
import string

import http.constants as constants

__all__ = (
    'Request'
)

class Request():
    _REQUEST_LINE_PATTERN = re.compile(r'^(?P<method>[A-Z]+)\s+' \
                                       r'((?P<scheme>http[s]?)://)?' \
                                       r'(?P<host>[\w*\.]*\w+)?/?' \
                                       r'(?P<path>[^\?]*)?(\?[^.]*)?(\#.*)?\s+' \
                                       r'(?P<http_ver>HTTP/1.[1|0])$')

    def __init__(self):
        self.method = None
        self.path = None
        self.headers = dict()


    def parse(self, raw_request):
        if not raw_request or type(raw_request) != str:
            return False
        
        if raw_request.find(constants.BODY_DELIMITER) > 0:
            request, _ = raw_request.split(constants.BODY_DELIMITER)
        else:
            request = raw_request
        
        if request.find(constants.STRING_DELIMITER) > 0:
            request_line, headers = request.split(constants.STRING_DELIMITER, maxsplit=1)
            return self._parse_headers(headers) and self._parse_request_line(request_line)
        else:
            request_line = request
            return self._parse_request_line(request_line)



    def _parse_headers(self, raw_headers):
        if not raw_headers or type(raw_headers) != str:
            return False
        
        headers_list = raw_headers.split(constants.STRING_DELIMITER)

        for header in headers_list:
            key, value = list(map(lambda x: x.strip(), header.split(':', maxsplit=1)))
            self.headers[key] = value

        return True


    def _parse_request_line(self, raw_request_line):
        if not raw_request_line or type(raw_request_line) != str:
            return False

        match = self._REQUEST_LINE_PATTERN.search(raw_request_line)

        if not match:
            return False

        self.method = match.group('method')
        self.path = match.group('path')

        #если путь ведет в родительские каталоги
        if self.path.find('/../') > 0:
            return False

        return True
