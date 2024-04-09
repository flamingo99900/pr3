#!/usr/bin/python3

import socket
import asyncio

          
class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def start(self):
        asyncio.run(self._async_start())
    
    async def handle_client(self):
        pass

    async def _async_start(self):
        server = await asyncio.start_server(
            self.handle_client, self._host, self._port)
        addr = server.sockets[0].getsockname()
        print(f'Сервер запущен на {addr}')
        async with server:
            await server.serve_forever()






