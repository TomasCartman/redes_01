import socket
import select
import json
from threading import Thread

HOST = ''
PORT = 50007
CHUNK_SIZE = 2048


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = list()
        self.readers = [self.server_socket]
        self.writers = list()
        self.command_list = ['listar', 'sair']

    def prepare_for_connection(self):
        self.server_socket.bind((HOST, PORT))
        self.server_socket.setblocking(False)
        self.server_socket.listen()
        print(f'Listing to port {PORT}')

    def run(self):
        try:
            t1 = Thread(target=self._run)
            t1.start()
            while True:
                command = str(input('Digite o comando: \n')).lower()
                if command in self.command_list:
                    if command == 'sair':
                        print('Fechando conexão...\n')
                        self.server_socket.close()
                    elif command == 'listar':
                        print('Clientes:\n')

                else:
                    print('Comando não encontrado.\n')
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            self.server_socket.close()
        except Exception as err:
            print(f'Error: {err}')
            self.server_socket.close()

    def _run(self):
        while True:
            readable, writeable, exceptional = select.select(self.readers,  self.writers, self.readers, 0.5)

            for s in readable:
                try:
                    if s == self.server_socket:
                        client_socket, address = s.accept()
                        client_socket.setblocking(False)
                        print(f'Connection from: {address[0]}:{address[1]}')
                        self.readers.append(client_socket)
                    else:
                        data = s.recv(CHUNK_SIZE)
                        if data:
                            obj = json.loads(data)
                            print(f'Recv from ?')
                            print(obj)
                            # self.writers.append(s)
                        else:
                            pass
                            # s.close()
                            # self.readers.remove(s)

                except Exception as err:
                    self.readers.remove(s)
                    s.close()
                    print(f'An error occurred: {err}')
                finally:
                    pass

            for s in writeable:
                try:
                    s.send(bytes('send', "utf-8"))
                    print('Sending')
                    self.writers.remove(s)
                except Exception as err:
                    print(f'An error occurred: {err}')
                finally:
                    pass

            for s in exceptional:
                pass



server = Server()
server.prepare_for_connection()
server.run()
server.server_socket.close()
