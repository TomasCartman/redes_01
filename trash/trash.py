import select
import socket
import config
from threading import Thread


class Trash:
    def __init__(self):
        self.thread1 = None
        self.trash_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inputs = []
        self.outputs = []
        self.message = ''

    def connect(self):
        try:
            self.trash_socket.connect((config.HOST, config.PORT))
            print(f'Connect at {config.HOST}:{config.PORT}')
            self.trash_socket.setblocking(False)
            self.inputs.append(self.trash_socket)
        except Exception as err:
            print('An error occurred while trying to connect to the server: ', err)

    def disconnect(self):
        self.thread1 = None
        self.trash_socket.close()

    def send_message_to_server(self, s, message):
        if type(message) is not bytes:  # Remove this (?)
            message = bytes(message, "utf-8")
        s.sendall(message)
        print(f'Sending: {message}')
        self.message = ''
        self.outputs.remove(s)
        self.inputs.append(s)

    def receive_message_from_server(self, s):
        try:
            server_response = s.recv(config.CHUNK_SIZE)
            self.inputs.remove(s)
            if server_response:
                return server_response.decode("utf-8")
        except Exception as err:
            print('An error occurred while trying to receive a message from the server: ', err)
            self.disconnect()

    def run(self):
        try:
            self.thread1 = Thread(target=self._run)
            self.thread1.start()

        except KeyboardInterrupt:
            print('Keyboard interrupt')
            self.disconnect()

        except Exception as err:
            print(f'Error: {err}')
            self.disconnect()

    def _run(self):
        while True:
            if self.message:
                self.outputs.append(self.trash_socket)
            readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0.5)

            for s in writeable:
                if s.fileno() < 0:
                    break
                self.send_message_to_server(s, self.message)

            for s in readable:
                if s == self.trash_socket and s.fileno() > 0:  # Test this
                    data = self.receive_message_from_server(s)
                    print(data)

            for s in exceptional:
                if s in self.inputs:
                    self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)

            if self.thread1 is None:
                break
