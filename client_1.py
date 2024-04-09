import socket

HOST = (socket.gethostname(), 4444)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(HOST)
print("Client conected to", HOST)

client.send('1'.encode('utf-8'))
while True:
    message = input("Введите скрипты для запуска в формате: [script1 {arg1 arg2}, script2]: ")
    client.send(message.encode('utf-8'))
    if message == "q":
        break

client.close()
