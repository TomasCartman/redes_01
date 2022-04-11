import os
import re
import socket
import uuid


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def get_mac_address():
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    return mac


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
