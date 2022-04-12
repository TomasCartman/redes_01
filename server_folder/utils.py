import os


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


# Zero included
def is_int_and_positive(string):
    try:
        value = int(string)
        if value >= 0:
            return True
        else:
            return False
    except ValueError:
        return False
