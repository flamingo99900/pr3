import socket

def send_command_to_server(command):
    HOST = socket.gethostname()
    PORT = 4444

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send('2'.encode('utf-8'))
        s.sendall(command.encode())

        received_data = b''
        while True:
            data = s.recv(1)
            if not data:
                break
            received_data += data

        print('Получено от сервера:', received_data.decode())

if __name__ == "__main__":
    user_command = input("Введите команду для сервера update: ")
    send_command_to_server(user_command)
