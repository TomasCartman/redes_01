import time
import client
import select
import truck_messages
import utils
import terminal_helper
from threading import Thread

command_list = ['sair', 'listar']


class Truck(client.Client):
    def __init__(self):
        super().__init__()
        self.trash_list = []

    def on_connect(self):
        self.message = truck_messages.dumps_object_start_on_json()

    def on_disconnect(self):
        self.message = truck_messages.dumps_object_close_on_json()
        time.sleep(1)

    def print_list_of_trashes(self):
        terminal_helper.print_trash_client(self.trash_list)

    def run(self):
        try:
            self.thread1 = Thread(target=self._run)
            self.thread1.start()
            while True:
                command = str(input('Digite o comando: \n')).lower()
                if command in command_list:
                    utils.clear_terminal()
                    if command == 'sair':
                        print('Fechando conexão...\n')
                        self.disconnect(self.on_disconnect)
                        break

                    elif command == 'listar':
                        self.print_list_of_trashes()

                else:
                    print('Comando não encontrado')

        except KeyboardInterrupt:
            print('Keyboard interrupt')
            self.disconnect(self.on_disconnect)

        except Exception as err:
            print(f'Error: {err}')
            self.disconnect()

    def _run(self):
        while True:
            if self.message:
                self.outputs.append(self.main_socket)

            readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0.5)

            for s in writeable:
                if s.fileno() < 0:
                    break
                self.send_message_to_server(s, self.message)

            for s in readable:
                if s == self.main_socket and s.fileno() > 0:
                    data = self.receive_message_from_server(s)
                    if data:
                        print(data)
                        if data['type'] == 'list':
                            self.trash_list = data['list']
                            print('Lista de lixeiras recebidas')

                    else:
                        print('Something went wrong. Closing connection')
                        self.disconnect()

            if self.thread1 is None:
                break


if __name__ == '__main__':
    truck = Truck()
    truck.connect(truck.on_connect)
    truck.run()
