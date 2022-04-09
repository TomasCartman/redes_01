import os


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
