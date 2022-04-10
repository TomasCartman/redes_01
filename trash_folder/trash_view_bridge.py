import time
import trash
import view
import trash_messages


class Bridge:
    def __init__(self):
        self.main_trash = trash.Trash(self.on_server_order_to_lock, self.on_server_order_to_unlock)
        self.main_view = view.TrashApp(self.on_view_change_callback, self.on_close_window_callback)

    def on_view_change_callback(self, trash_capacity, trash_filled, trash_status):
        print(f'trash_capacity: {trash_capacity} and trash_filled: {trash_filled}; trash is locked: {trash_status}')
        self.send_message_update_to_server(trash_capacity, trash_filled, trash_status)

    def send_message_update_to_server(self, trash_capacity, trash_filled, trash_status):
        obj = trash_messages.dumps_object_update_on_json(trash_capacity, trash_filled, trash_status)
        self.main_trash.message = obj

    def send_message_start_to_server(self):
        obj = trash_messages.dumps_object_start_on_json()
        self.main_trash.message = obj

    def send_message_close_to_server(self):
        obj = trash_messages.dumps_object_close_on_json()
        self.main_trash.message = obj

    def on_close_window_callback(self):
        print('Disconnecting...')
        self.send_message_close_to_server()
        time.sleep(1)
        self.main_trash.disconnect()

    def on_server_order_to_lock(self):
        self.main_view.lock_trash_button_callback()

    def on_server_order_to_unlock(self):
        self.main_view.unlock_trash()

    def trash_connect_and_run(self):
        self.main_trash.connect()
        self.main_trash.run()
        self.send_message_start_to_server()

    def start_view_main_loop(self):
        self.main_view.mainloop()

    def run(self):
        self.trash_connect_and_run()
        self.start_view_main_loop()


if __name__ == '__main__':
    Bridge().run()
