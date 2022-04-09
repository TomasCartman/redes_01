import json
import utils


def load_object_start_on_json():
    start_info = {
        'type': 'start',
        'sender': 'trash',
        'mac': utils.get_mac_address()
    }
    obj = json.dumps(start_info)
    return obj


def load_object_update_on_json(trash_capacity, trash_filled, trash_status):
    update_info = {
        'type': 'update',
        'sender': 'trash',
        'trash_capacity': trash_capacity,
        'trash_filled': trash_filled,
        'trash_status': trash_status,
        'mac': utils.get_mac_address()
    }
    obj = json.dumps(update_info)
    return obj


def load_object_close_on_json():
    close_info = {
        'type': 'close',
        'sender': 'trash',
        'mac': utils.get_mac_address()
    }
    obj = json.dumps(close_info)
    return obj
