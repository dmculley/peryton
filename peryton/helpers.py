"""
.. module:: helpers
   :synopsis: This module holds various helper functions and classes. These are
    mostly related to computational housekeeping rather than anything directly
    modelling related.

"""

from firedrake import *


def info_out(msg, colour=None, bold=False, underline=False, comm=COMM_WORLD):
    """ Prints the passed message

    :param msg: The message to be printed
    :type msg: string
    :param colour: The colour of the message - red, yellow, green, blue, purple
    :type colour: string
    :param bold: Whether the message should be printed in bold
    :type bold: bool
    :param underline: Whether the message should be printed underline
    :type underline: bool
    """
    unicoding = True
    if comm.rank == 0:
        if unicoding:
            if colour == 'red':
                msg = '\033[91m' + msg + '\033[0m'
            elif colour == 'yellow':
                msg = '\033[93m' + msg + '\033[0m'
            elif colour == 'green':
                msg = '\033[92m' + msg + '\033[0m'
            elif colour == 'blue':
                msg = '\033[94m' + msg + '\033[0m'
            elif colour == 'purple':
                msg = '\033[95m' + msg + '\033[0m'
            elif colour == 'orange':
                msg = '\033[33m' + msg + '\033[0m'
            if bold:
                msg = '\033[1m' + msg + '\033[0m'
            if underline:
                msg = '\033[4m' + msg + '\033[0m'
        print(msg)
