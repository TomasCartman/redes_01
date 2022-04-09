import trash
import view
import json


def load_object_on_json(trash_capacity, trash_filled, trash_status):
    trash_info = {
        'sender': 'trash',
        'trash_capacity': trash_capacity,
        'trash_filled': trash_filled,
        'trash_status': trash_status,
        'mac': trash.get_mac_address()
    }
    obj = json.dumps(trash_info)
    return obj


class Bridge:
    def __init__(self):
        self.main_trash = trash.Trash()
        self.main_view = view.TrashApp(self.on_view_change_callback, self.on_close_window_callback)

    def on_view_change_callback(self, trash_capacity, trash_filled, trash_status):
        print(f'trash_capacity: {trash_capacity} and trash_filled: {trash_filled}; trash is locked: {trash_status}')
        self.send_message_to_server(trash_capacity, trash_filled, trash_status)

    def send_message_to_server(self, trash_capacity, trash_filled, trash_status):
        obj = load_object_on_json(trash_capacity, trash_filled, trash_status)
        self.main_trash.message = obj

    def on_close_window_callback(self):
        print('Disconnecting...')
        self.main_trash.disconnect()

    def trash_connect_and_run(self):
        self.main_trash.connect()
        self.main_trash.run()

    def start_view_main_loop(self):
        self.main_view.mainloop()

    def run(self):
        self.trash_connect_and_run()
        self.start_view_main_loop()


if __name__ == '__main__':
    Bridge().run()
