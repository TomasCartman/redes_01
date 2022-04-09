import json


def load_object_lock_on_json():
    lock_info = {
        'type': 'lock',
        'sender': 'server'
    }
    obj = json.dumps(lock_info)
    return obj.encode("utf-8")


def load_object_unlock_on_json():
    lock_info = {
        'type': 'unlock',
        'sender': 'server'
    }
    obj = json.dumps(lock_info)
    return obj.encode("utf-8")
