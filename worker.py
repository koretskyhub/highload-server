import asyncio
import mimetypes
import os
import socket
from datetime import datetime
from urllib.parse import unquote

import request
from response import Response


class Worker:
    _CHUNK_SIZE = 1024
    _ALLOWED_METHODS = ('GET', 'HEAD')
    _INDEX_FILE = 'index.html'

    def __init__(self, socket, document_root):
         self.socket = socket
         self.document_root = os.path.abspath(document_root)
         self.request_parser = request.Request()

         self.loop = asyncio.get_event_loop()
         asyncio.set_event_loop(self.loop)
         self.loop.run_until_complete(self._run_worker())


    async def _run_worker(self):
        while True:
            conn, addr = await self.loop.sock_accept(self.socket)
            print('client connected ', datetime.utcnow())
            self.loop.create_task(self.handle_connection(conn))


    async def _read(self, sock):
        return (await self.loop.sock_recv(sock, self._CHUNK_SIZE)).decode('utf8')


    async def _write(self, socket, response, file_path = None):
        await self.loop.sock_sendall(socket, str(response).encode('utf-8'))
        
        if file_path is not None:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda : f.read(self._CHUNK_SIZE), b''):
                    await self.loop.sock_sendall(socket, chunk)


    async def handle_connection(self, socket):
        request = await self._read(socket)
 
        if not self.request_parser.parse(request):
            await self._write(socket, Response(400))
            socket.close()
            print('cannot parse request')
            return

        if self.request_parser.method not in self._ALLOWED_METHODS:
            await self._write(socket, Response(405))
            socket.close()
            print('method not allowed')
            return


        file_path = self.request_parser.path

        #path не должен начинаться со /
        file_path = os.path.join(self.document_root, self.request_parser.path)
        file_path = unquote(file_path)
        file_path = os.path.abspath(file_path)

        print('requested path is: ', file_path)


        if not os.path.exists(file_path):
            await self._write(socket, Response(403))
            socket.close()
            print('path: ', file_path, ' does not exist')
            return

        dir_requested = False

        if os.path.isdir(file_path):
            dir_requested = True
            file_path = os.path.join(file_path, self._INDEX_FILE)
            if not os.path.exists(file_path):
                await self._write(socket, Response(403))
                socket.close()
                print(self._INDEX_FILE, 'does not exist at parent directory')
                return

        if os.path.isfile(file_path):
            if self.request_parser.path.endswith('/') and not dir_requested:
                print('file', file_path, 'requested as directory')
                await self._write(socket, Response(404))
            else:
                mime_type, _ = mimetypes.guess_type(file_path)
                headers = {
                    'Content-Length': str(os.path.getsize(file_path)),
                    'Content-Type': mime_type,
                }
                print('returning 200')
                await self._write(socket, Response(200, headers_dict = headers), file_path)
            socket.close()
            return
