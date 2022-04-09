import socket
import select
import json
import os
from threading import Thread

HOST = ''
PORT = 50007
CHUNK_SIZE = 2048


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


class Server:
    def __init__(self):
        self.thread1 = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = list()
        self.readers = [self.server_socket]
        self.writers = list()
        self.command_list = ['clientes', 'sair', 'travar', 'help', 'socket']

    def prepare_for_connection(self):
        self.server_socket.bind((HOST, PORT))
        self.server_socket.setblocking(False)
        self.server_socket.listen()
        print(f'Listing to port {PORT}')

    def disconnect(self):
        self.thread1 = None
        self.server_socket.close()

    def filter_clients(self):
        for c in self.clients:
            if c['client_socket'].fileno() < 0:
                self.clients.remove(c)

    def list_clients(self):
        clients = []
        counter = 0
        for c in self.clients:
            if c['mac'] != '':
                counter += 1
                client = {
                    'ip_address': c['address'],
                    'mac': c['mac'],
                    'trash_capacity': c['trash']['trash_capacity'],
                    'trash_filled': c['trash']['trash_filled'],
                    'trash_status': c['trash']['trash_status']
                }
                clients.append(client)
        return clients, counter

    def print_clients(self):
        clients, number_of_clients = self.list_clients()
        print(f'Clientes: [{number_of_clients}]\n')
        for c in clients:
            trash_percentage = (c["trash_filled"]/c["trash_capacity"])*100
            print(f'Address: {c["ip_address"]} ou Mac: {c["mac"]}')
            print(f'Lixeira {trash_percentage:,.2f}% cheia ({c["trash_filled"]}/{c["trash_capacity"]})')
            print(f'Lixeira {"travada" if c["trash_status"] else "destravada"}\n')

    def run(self):
        try:
            self.thread1 = Thread(target=self._run)
            self.thread1.start()
            while True:
                command = str(input('Digite o comando: \n')).lower()
                if command in self.command_list:
                    clear_terminal()
                    if command == 'sair':
                        print('Fechando conexão...\n')
                        self.disconnect()
                        break
                    elif command == 'clientes':
                        self.filter_clients()
                        self.print_clients()
                        print('\n')
                    elif command == 'socket':
                        print(self.clients)

                else:
                    print('Comando não encontrado.\n')
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            self.disconnect()
        except Exception as err:
            print(f'Error: {err}')
            self.disconnect()

    def _run(self):
        while True:
            if self.thread1 is None:
                break

            readable, writeable, exceptional = select.select(self.readers, self.writers, self.readers, 0.5)

            for s in readable:
                try:
                    if s == self.server_socket:
                        client_socket, address = s.accept()
                        client_socket.setblocking(False)
                        client = {
                            'client_socket': client_socket,
                            'address': address[0],
                            'mac': ''
                        }
                        print(f'Connection from: {address[0]}:{address[1]}')
                        self.clients.append(client)
                        self.readers.append(client_socket)
                    else:
                        data = s.recv(CHUNK_SIZE)
                        if data:
                            obj = json.loads(data)
                            if obj['sender'] == 'trash':
                                mac = obj['mac']
                                res = next(item for item in self.clients if item['client_socket'] == s)
                                if res:
                                    if res['mac'] == '':
                                        res['mac'] = mac
                                    res['trash'] = obj

                                print(f'Recv from {mac}')
                                print(obj)
                            else:  # Not a trash, so it's a truck
                                pass
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


if __name__ == '__main__':
    server = Server()
    server.prepare_for_connection()
    server.run()
    server.disconnect()   # Remove this
