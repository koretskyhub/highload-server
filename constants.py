from datetime import datetime

HTTP_VERSION = '1.1'
SERVER_NAME = 'AsyncIO'
STRING_DELIMITER = '\r\n'
BODY_DELIMITER = '\r\n' * 2
CHUNK_SIZE = 1024
QUEUE_SIZE = 8
ALLOWED_METHODS = ('GET', 'HEAD')
INDEX_FILE = 'index.html'

HTTP_STATUS_MESSAGES = {
    200 : 'OK',
    403 : 'Forbidden',
    404 : 'Not Found',
    405 : 'Method Not Allowed',
}

def default_headers(self):
        return {
        'Connection': 'close',
        'Date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
        'Server': self._SERVER_NAME
    }