import socket
import select
import time

HOST = '127.0.0.1'
PORT = 50007
CHUNK_SIZE = 2048


class Trash:
    def __init__(self):
        self.trash_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inputs = []
        self.outputs = [self.trash_socket]

    def connect(self):
        try:
            self.trash_socket.connect((HOST, PORT))
            print(f'Connect at {HOST}:{PORT}')
            self.trash_socket.setblocking(False)
        except Exception as err:
            print('An error occurred while trying to connect to the server: ', err)

    # A check must take place (is the socket connected?) before trying to disconnect | Not using
    def disconnect(self):
        self.trash_socket.close()

    def send_message_to_server(self, s, message):
        s.sendall(bytes(message, "utf-8"))
        print('Sending')
        self.outputs.remove(s)
        self.inputs.append(s)

    def receive_message_from_server(self, s):
        try:
            server_response = s.recv(CHUNK_SIZE)
            self.inputs.remove(s)
            self.outputs.append(s)
            if server_response:
                return server_response.decode("utf-8")
        except Exception as err:
            print('An error occurred while trying to receive a message from the server: ', err)
            self.disconnect()

    def run(self):
        try:
            while True:
                time.sleep(1.5)
                readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0.5)

                for s in writeable:
                    self.send_message_to_server(s, 'Testing...\n')

                for s in readable:
                    data = self.receive_message_from_server(s)
                    print('recv')

                for s in exceptional:
                    pass
        except KeyboardInterrupt:
            print('Keyboard interrupt')


t = Trash()
t.connect()
t.run()
t.disconnect()
# t.connect()
# t.send_message_to_server(bytes('Testing...', "utf-8"))
# response = t.receive_message_from_server()
# t.disconnect()
# print(response)


'''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    try:
        while True:
            msg = bytes(input('To server: ').encode("utf-8"))
            s.sendall(msg)
            data = s.recv(CHUNK_SIZE)
            print(data.decode("utf-8"))
    except KeyboardInterrupt:
        print('Caught KeyboardInterrupt')
        s.close()
    except ConnectionResetError:
        print('Connection was forcibly closed by the host')
    finally:
        s.close()
    s.close()
'''
