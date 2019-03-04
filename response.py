from datetime import datetime
import constants

__all__ = (
    'Response'
)


class Response:
    def __init__(self, status_code, headers_dict={}):
        self.status_code = status_code
        self.headers_dict = headers_dict


    def _default_headers(self):
        return {
            'Connection': 'close',
            'Date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'Server': constants.SERVER_NAME
        }


    def build_headers(self, headers_dict):
        headers_dict = {**headers_dict, **self._default_headers()}
        return constants.STRING_DELIMITER.join(
            "{!s}: {!s}".format(key, val) for (key, val) in headers_dict.items())


    def build_response_line(self, status):
        message = constants.HTTP_STATUS_MESSAGES.get(status) or ''
        return 'HTTP/{} {} {}'.format(constants.HTTP_VERSION, status, message)


    def __str__(self):
        response_line = self.build_response_line(self.status_code)
        headers = self.build_headers(self.headers_dict)
        return r'{}{}{}{}'.format(response_line, constants.STRING_DELIMITER, headers, constants.BODY_DELIMITER)
