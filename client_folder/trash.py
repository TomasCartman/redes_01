import trash_messages
import time
import select
import client
from threading import Thread


class Trash(client.Client):
    def __init__(self, lock_callback, unlock_callback, on_error):
        super().__init__()
        self.lock_callback = lock_callback
        self.unlock_callback = unlock_callback
        self.on_error = on_error

    def _lock_trash(self):
        self.lock_callback()

    def _unlock_trash(self):
        self.unlock_callback()

    def on_connect(self):
        self.message = trash_messages.dumps_object_start_on_json()

    def on_disconnect(self):
        self.message = trash_messages.dumps_object_close_on_json()
        time.sleep(1)

    def run(self):
        try:
            self.thread1 = Thread(target=self._run)
            self.thread1.start()

        except KeyboardInterrupt:
            print('Keyboard interrupt')
            self.disconnect()
            self.on_error()

        except Exception as err:
            print(f'Error: {err}')
            self.disconnect()
            self.on_error()

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
                        if data['type'] == 'lock':
                            self._lock_trash()

                        elif data['type'] == 'unlock':
                            self._unlock_trash()

                    else:
                        print('Something went wrong. Closing connection')
                        self.disconnect()
                        self.on_error()
            '''
            for s in exceptional:
                if s in self.inputs:
                    self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
            '''
            if self.thread1 is None:
                break
