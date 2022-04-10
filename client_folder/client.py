import socket
import config
import json


def _null():
    pass


class Client:
    def __init__(self):
        self.thread1 = None
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inputs = []
        self.outputs = []
        self.message = ''

    def connect(self, on_connect):
        try:
            self.main_socket.connect((config.HOST, config.PORT))
            print(f'Connect at {config.HOST}:{config.PORT}')
            self.main_socket.setblocking(False)
            self.inputs.append(self.main_socket)
            on_connect()
        except Exception as err:
            print('An error occurred while trying to connect to the server: ', err)

    def disconnect(self, on_disconnect=_null):
        on_disconnect()
        self.thread1 = None
        self.main_socket.close()

    def send_message_to_server(self, s, message):
        s.sendall(message)
        print(f'Sending: {message}')
        self.message = ''
        self.outputs.remove(s)

    def receive_message_from_server(self, s):
        try:
            server_response = s.recv(config.CHUNK_SIZE)
            if server_response:
                response_decoded = server_response.decode("utf-8")
                return json.loads(response_decoded)
        except Exception as err:
            print('An error occurred while trying to receive a message from the server: ', err)
            self.disconnect()

    def run(self):
        pass

    def _run(self):
        pass
