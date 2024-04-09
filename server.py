#!/usr/bin/python3

import socket
import asyncio
import os
import json
import datetime

def get_processes_info():
    process = []
    for line in os.popen('tasklist').readlines()[3:]:
        split_line = line.split()
        if len(split_line) >= 5:
            process.append({
                'Name': split_line[0],
                'PID': split_line[1],
                'Session Name': split_line[2],
                'Session#': split_line[3],
                'Memory Usage': split_line[4]
            })
    return process


def save_to_json(process, filename):
    with open(filename, 'w') as f:
        json.dump(process, f, indent=4)
    print(f"Сохранено в JSON файл: {filename}")
          
class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def start(self):
        asyncio.run(self._async_start())
    
    async def handle_client(self, reader, writer):
        res = None
        input_data = await reader.read(1)
        input_data = input_data.decode('utf-8')

        if input_data == "2":
            print("polina")
            res = await self.polina(reader)
        if res:
            writer.write(res.encode('utf-8'))
            writer.close()
            await writer.wait_closed()


    async def _async_start(self):
        server = await asyncio.start_server(
            self.handle_client, self._host, self._port)
        addr = server.sockets[0].getsockname()
        print(f'Сервер запущен на {addr}')
        async with server:
            await server.serve_forever()

    async def polina(self, reader):
        data = ""
        while True:
            request = await reader.read(1)
            if request:
                data += request.decode()
                if data == "update":
                    process = get_processes_info()
                    now = datetime.now()
                    folder_name = now.strftime("%d-%m-%Y")
                    filename = now.strftime("%H-%M-%S")
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    save_to_json(process, f"{folder_name}/{filename}.json")
                    s = f'Сохранено в файл: {filename}.json'
                    return s





if __name__ == "__main__":
    HOST = socket.gethostname()
    PORT = 4444
    server = Server(HOST, PORT)
    server.start()


