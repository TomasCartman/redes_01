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
