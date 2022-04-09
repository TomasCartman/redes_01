import json
from client_folder import utils


def dumps_object_start_on_json():
    start_info = {
        'type': 'start',
        'sender': 'truck',
        'mac': utils.get_mac_address()
    }
    obj = json.dumps(start_info)
    return obj.encode("utf-8")


def dumps_object_close_on_json():
    close_info = {
        'type': 'close',
        'sender': 'truck',
        'mac': utils.get_mac_address()
    }
    obj = json.dumps(close_info)
    return obj.encode("utf-8")
