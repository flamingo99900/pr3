#!/usr/bin/python3

import socket
import asyncio
import os
import json
from datetime import datetime
import subprocess



def load_program_data():
    if os.path.exists("program_data.json"):
        with open("program_data.json", "r") as json_file:
            return json.load(json_file)
    else:
        return []


class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.server = None


    def start(self):
        asyncio.run(self._async_start())
    
    async def handle_client(self,  reader, writer):
        res = None
        input_data = await reader.read(1)
        input_data = input_data.decode('utf-8')
        if input_data == "1":
            print("roma")
            res = await self.roma(reader)
        
        if res:
            writer.write(res.encode('utf-8'))
            writer.close()
            await writer.wait_closed()


    async def roma(self, reader):
        programs = {"dir", "echo 1"}
        program_data = load_program_data()  # добавляю программы, вызванные во время предыдущих запусков кода
        if program_data:
            for i in program_data:
                programs.add(i["program"])
        data = ""
        while True:
            request = await reader.read(1)
            if request:
                if request.decode() != "q":
                    data += request.decode()
                if request.decode() == "q":
                    break
        if data:  # добавляю программы клиента к списку всех программ
            new_programs = set()
            print("DATA FROM CLIENT:\n", data, "\n")
            for program in data.split(","):
                new_programs.add(program)
            programs.update(new_programs)
        print(programs)
        for program in programs:
            print(program)
            # Создаем папку с именем программы, если она еще не существует
            if not os.path.exists(program):
                os.makedirs(program)

            # Получаем текущую дату и время
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y %m %d %H %M %S")

            # Создаем имя файла в формате "ГГГГ ММ ДД ЧЧ ММ СС"
            output_file_name = f"{formatted_datetime}.txt"

            # Создаем файл для вывода
            output_file = os.path.join(program, output_file_name)

            # Запускаем программу и записываем её вывод в файл
            with open(output_file, "w") as f:
                process = subprocess.run(program, shell=True, capture_output=True, text=True)
                output = process.stdout.encode('cp1251').decode('cp866')
                print(output)
                f.write(output)

            # Добавляем информацию о программе, папке и файле в список
            program_data.append({
                "program": program,
                "folder": program,
                "file": output_file
            })

        # Сохраняем информацию в файл JSON
        with open("program_data.json", "w") as json_file:
            json.dump(program_data, json_file, indent=4)

        return "Успешно"


    async def _async_start(self):
        server = await asyncio.start_server(
            self.handle_client, self._host, self._port)
        addr = server.sockets[0].getsockname()
        print(f'Сервер запущен на {addr}')
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    HOST = socket.gethostname()
    PORT = 4444
    server = Server(HOST, PORT)
    server.start()



