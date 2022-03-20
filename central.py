import socket

HOST = ''
PORT = 50007
CHUNK_SIZE = 2048


def accept_connection(s):
    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        while True:
            data = conn.recv(CHUNK_SIZE)
            if not data:
                print(f'Disconnected by {addr}')
                break
            print(data.decode("utf-8"))
            conn.sendall(b'Message was received')
    s.close()


try:
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen()
            accept_connection(s)
        except KeyboardInterrupt:
            print('Caught KeyboardInterrupt')
            s.close()
except:
    pass


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
