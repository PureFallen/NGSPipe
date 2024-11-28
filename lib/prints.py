import datetime

from .colors import BColors


def print_info(info_string):
    print(f'{BColors.PURPLE}{timestamp()}[INFO]  {BColors.WHITE}{info_string}{BColors.RESET}')


def print_error(err_string):
    print(f'{BColors.RED}{timestamp()}[ERROR] {err_string}{BColors.RESET}')


def timestamp():
    x = datetime.datetime.now()
    return x.strftime('[%d.%m.%y %H:%M:%S]')
