import socket
import select
import json
import time
import config
import utils
import server_messages
import terminal_helper
from threading import Thread

command_list = ['clientes', 'sair', 'travar', 'help', 'socket', 'destravar', 'caminhao', 'gerar_lista',
                'enviar_caminhao', 'lixeiras', 'modificar_lista', 'lista', 'clean']


def list_client(trash_client):
    if 'trash' in trash_client:
        client = {
            'id': trash_client['id'],
            'ip_address': trash_client['address'],
            'mac': trash_client['mac'],
            'trash_capacity': trash_client['trash']['trash_capacity'],
            'trash_filled': trash_client['trash']['trash_filled'],
            'trash_status': trash_client['trash']['trash_status']
        }
        return client
    else:
        return False


class Server:
    def __init__(self):
        self.thread1 = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.trash_clients = list()
        self.truck_clients = list()
        self._number_of_clients = 0
        self.readers = [self.server_socket]
        self.writers = list()
        self.list_to_send_to_truck = list()

    def prepare_for_connection(self):
        self.server_socket.bind((config.HOST, config.PORT))
        self.server_socket.setblocking(False)
        self.server_socket.listen()
        print(f'Listing to port {config.PORT}')

    def disconnect(self):
        print('Fechando conexão...\n')
        self.close_all_client_connections()
        self.thread1 = None
        self.server_socket.close()

    def close_all_client_connections(self):
        for c in self.readers:
            if c != self.server_socket:
                self.readers.remove(c)
                c.sendall(server_messages.dumps_object_close_on_json())
        time.sleep(1)
        for c in self.readers:
            if c != self.server_socket:
                c.close()

    def list_clients(self):
        clients = []
        for c in self.trash_clients:
            client = list_client(c)
            if client:
                clients.append(client)
        return clients

    def order_trashes(self):
        trash_clients = self.list_clients()
        ordered_trash_clients = sorted(trash_clients, reverse=True,
                                       key=lambda c: (int(c['trash_filled']) / int(c['trash_capacity'])))
        return ordered_trash_clients

    def filter_trash_list_by_threshold(self, percentage=0.75):
        ordered_trash_clients = self.order_trashes()
        filtered_ordered_trash_clients = []
        for c in ordered_trash_clients:
            if int(c['trash_filled']) / int(c['trash_capacity']) >= percentage:
                filtered_ordered_trash_clients.append(c)
        return filtered_ordered_trash_clients

    def print_clients(self):
        clients = self.list_clients()
        print(f'Clientes: [{len(clients)}]\n')
        terminal_helper.print_trash_client(clients)

    def print_ordered_trashes(self):
        ordered_trash_clients = self.order_trashes()
        terminal_helper.print_trash_client(ordered_trash_clients)

    def print_to_send_to_truck_list(self):
        terminal_helper.print_trash_client(self.list_to_send_to_truck)

    def make_list_to_send_to_truck(self):
        filtered_ordered_trash_clients = self.filter_trash_list_by_threshold()
        self.list_to_send_to_truck = filtered_ordered_trash_clients
        print('A lista foi criada')

    def modify_list_to_send_to_truck(self, identifier, position):
        position = int(position)
        identifier = int(identifier)
        res = next((item for item in self.list_to_send_to_truck if item['id'] == identifier), False)
        if res:  # Trash is already in the list, change its position
            trash_index = self.list_to_send_to_truck.index(res)
            if position == trash_index:  # The trash is already on the position it should
                print(f'Lixeira {identifier}: {trash_index} -> {position}')

            elif position >= len(self.list_to_send_to_truck):  # It will be inserted on the last position
                self.list_to_send_to_truck.remove(res)
                self.list_to_send_to_truck.append(res)

            else:
                if position > trash_index:
                    self.list_to_send_to_truck.remove(res)
                    self.list_to_send_to_truck.insert(position, res)

                else:
                    self.list_to_send_to_truck.remove(res)
                    self.list_to_send_to_truck.insert(position, res)

        else:  # Trash is not on the list, include it
            trash_client = next((item for item in self.trash_clients if item['id'] == identifier), False)
            if trash_client:
                client = list_client(trash_client)
                if client:
                    self.list_to_send_to_truck.insert(position, client)

            else:
                print('Id não encontrado')

    def send_trash_list_to_truck(self):
        if len(self.truck_clients) > 0:
            trashes_list = self.list_to_send_to_truck
            sock = self.truck_clients[0]['client_socket']
            list_to_truck_info = server_messages.object_list_of_trashes_skeleton()
            list_to_truck_info['list'] = trashes_list
            obj = json.dumps(list_to_truck_info)
            obj_encoded = obj.encode("utf-8")
            sock.sendall(obj_encoded)
            self.list_to_send_to_truck = []
            print('As lixeiras foram enviadas para o caminhão')
        else:
            print('Não há um caminhão conectado')

    def handle_start_of_client(self, obj, sock):
        print('Start of client')
        client = {
            'client_socket': sock,
            'address': sock.getpeername()[0],
            'mac': obj['mac']
        }
        if obj['sender'] == 'trash':
            self._number_of_clients += 1
            client['id'] = self._number_of_clients
            self.trash_clients.append(client)
        else:
            print('truck connected')
            self.truck_clients.append(client)

    def handle_close_of_client(self, obj, sock):
        print('Close of client')
        self.readers.remove(sock)
        if obj['sender'] == 'trash':
            for i in range(len(self.trash_clients)):
                if self.trash_clients[i]['client_socket'] == sock:
                    del self.trash_clients[i]
                    break
        else:
            self.truck_clients.pop()

    # Only the trash updates the server, so there's no need to verify if it's a truck or trash
    def handle_update_of_client(self, obj, sock):
        print('Update of client')
        res = next(item for item in self.trash_clients if item['client_socket'] == sock)
        if res:
            res['trash'] = {
                'trash_capacity': obj['trash_capacity'],
                'trash_filled': obj['trash_filled'],
                'trash_status': obj['trash_status'],
            }

    def lock_trash(self, identifier):
        res = next((item for item in self.trash_clients if item['id'] == identifier), False)
        if res:
            sock = res['client_socket']
            print(f'sending: {server_messages.dumps_object_lock_on_json()}')
            sock.sendall(server_messages.dumps_object_lock_on_json())
        else:
            print('Lixeira não encontrada, verifque a lista de clientes e tente novamente.\n')

    def unlock_trash(self, identifier):
        res = next((item for item in self.trash_clients if item['id'] == identifier), False)
        if res:
            sock = res['client_socket']
            print(f'sending: {server_messages.dumps_object_unlock_on_json()}')
            sock.sendall(server_messages.dumps_object_unlock_on_json())
        else:
            print('Lixeira não encontrada, verifque a lista de clientes e tente novamente.\n')

    def get_command_and_run_functions(self):
        command_typed = str(input('Digite o comando: \n')).lower().split(' ')
        command = command_typed[0]
        if command in command_list:
            utils.clear_terminal()
            if command == 'sair':
                self.disconnect()

            elif command == 'help':
                terminal_helper.print_help()

            elif command == 'clientes':
                self.print_clients()

            elif command == 'socket':
                print(self.trash_clients)

            elif command == 'travar':
                if len(command_typed) != 2 or not utils.is_int(command_typed[1]):
                    print('Argumentos fornecidos são inválidos')
                else:
                    self.lock_trash(int(command_typed[1]))

            elif command == 'destravar':
                if len(command_typed) != 2 or not utils.is_int(command_typed[1]):
                    print('Argumentos fornecidos são inválidos')
                else:
                    self.unlock_trash(int(command_typed[1]))

            elif command == 'caminhao':
                print(self.truck_clients)

            elif command == 'lista':
                self.print_to_send_to_truck_list()

            elif command == 'lixeiras':
                self.print_ordered_trashes()

            elif command == 'gerar_lista':
                self.make_list_to_send_to_truck()

            elif command == 'modificar_lista':
                if len(command_typed) != 3 or not utils.is_int_and_positive(command_typed[1]) \
                        or not utils.is_int_and_positive(command_typed[2]):
                    print('Argumentos fornecidos são inválidos')
                else:
                    self.modify_list_to_send_to_truck(command_typed[1], command_typed[2])

            elif command == 'enviar_caminhao':
                self.send_trash_list_to_truck()

            elif command == 'clean':
                utils.clear_terminal()

        else:
            print('Comando não encontrado.\n')

    def run(self):
        try:
            self.thread1 = Thread(target=self._run)
            self.thread1.start()
            while True:
                self.get_command_and_run_functions()
                if self.thread1 is None:
                    break

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
                    # If the server socket is readable (means that there's a connection to accept)
                    if s == self.server_socket:
                        client_socket, address = s.accept()
                        client_socket.setblocking(False)
                        print(f'Connection from: {address[0]}:{address[1]}')
                        self.readers.append(client_socket)

                    else:  # An already accepted client socket is sending a message
                        data = s.recv(config.CHUNK_SIZE)
                        if data:
                            obj = json.loads(data)
                            if obj['type'] == 'start':  # First contact of the server and client
                                self.handle_start_of_client(obj, s)

                            elif obj['type'] == 'update':  # A client known by the server is updating its status
                                self.handle_update_of_client(obj, s)

                            else:  # The last contact of the client with the server
                                self.handle_close_of_client(obj, s)

                        else:
                            if s in self.readers:
                                self.readers.remove(s)
                            s.close()

                except Exception as err:
                    if s in self.readers:
                        self.readers.remove(s)
                    s.close()
                    print(f'An error occurred (readable): {err}')

            for s in writeable:
                try:
                    s.send(bytes('send', "utf-8"))
                    print('Sending')
                    self.writers.remove(s)
                except Exception as err:
                    print(f'An error occurred (writable): {err}')


if __name__ == '__main__':
    server = Server()
    server.prepare_for_connection()
    server.run()
