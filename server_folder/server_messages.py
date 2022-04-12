import json


def dumps_object_lock_on_json():
    lock_info = {
        'type': 'lock',
        'sender': 'server'
    }
    obj = json.dumps(lock_info)
    return obj.encode("utf-8")


def dumps_object_unlock_on_json():
    lock_info = {
        'type': 'unlock',
        'sender': 'server'
    }
    obj = json.dumps(lock_info)
    return obj.encode("utf-8")


#  Need to be dumped and then encoded
def object_list_of_trashes_skeleton():
    skeleton_info = {
        'type': 'list',
        'sender': 'server'
    }
    return skeleton_info


def dumps_object_close_on_json():
    close_info = {
        'type': 'close',
        'sender': 'server'
    }
    obj = json.dumps(close_info)
    return obj.encode("utf-8")

