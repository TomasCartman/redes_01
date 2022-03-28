import socket
import select
import time
import pickle

HOST = ''
PORT = 50007
CHUNK_SIZE = 2048


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = list()
        self.readers = [self.server_socket]
        self.writers = list()

    def prepare_for_connection(self):
        self.server_socket.bind((HOST, PORT))
        self.server_socket.setblocking(False)
        self.server_socket.listen()
        print(f'Listing to port {PORT}')

    def run(self):
        try:
            while True:
                #time.sleep(1.5)
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
                                obj = pickle.loads(data)
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

        except KeyboardInterrupt:
            print('Keyboard interrupt')


server = Server()
server.prepare_for_connection()
server.run()
server.server_socket.close()

'''
    def accept_connection(self):
        client_socket, address = self.server_socket.accept()
        i = 0
        while True:
            data = client_socket.recv(CHUNK_SIZE)
            print(f'{i} -> {data.decode("utf-8")}')
            #if i % 3 == 0:
            client_socket.sendall(bytes(f'{i}', "utf-8"))
            i += 1
            time.sleep(2)
        print(f'Client connected: {address[0]}:{address[1]}')
        self.clients.append(client_socket)

    def receive_from_trashes(self):
        pass
        #for client_socket in self.clients:
        #    print(client_socket)
        #while True:
        #    data = self.
'''


'''
def accept_connection(s):
    client_socket, address = s.accept()
    with client_socket:
        print(f'Connected by {address}')
        while True:
            data = client_socket.recv(CHUNK_SIZE)
            if not data:
                print(f'Disconnected by {address}')
                break
            print(data.decode("utf-8"))
            client_socket.sendall(b'Message was received')
    s.close()


try:
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen()
            print('Server started')
            accept_connection(s)
        except KeyboardInterrupt:
            print('Caught KeyboardInterrupt')
            s.close()
except:
    pass
'''
""""
    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        try:
            while True:
                data = conn.recv(CHUNK_SIZE)
                if data:
                    print(data.decode("utf-8"))
                    conn.sendall(b'Message was received')
        except KeyboardInterrupt:
            print('Caught KeyboardInterrupt')
            s.close()
    s.close()
"""
