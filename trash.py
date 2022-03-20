import socket

HOST = '127.0.0.1'
PORT = 50007
CHUNK_SIZE = 2048

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
