"""

Peryton - a steady-state RANS solver

"""

# Doc strings
__author__     = 'Dave Culley'
__copywrite__  = 'Copyright 2016, Dave Culley'
__version__    = 'Development'
__maintainer__ = 'Dave Culley'
__email__      = 'dmculley@gmail.com'
__status__     = 'PRE-RELEASE: early development'


# Import the modules for the package
from helpers import *
from problem import *
from domain import *
from boundary_conditions import *
from initial_conditions import *
from solvers import *
from navier_stokes import *


# Print welcome message
import time
import subprocess
from mpi4py import MPI
msg = '\n\nPeryton \nSteady-state RANS solver\n'
info_out(msg)
msg = time.strftime("%d/%m/%Y - %H:%M:%S") + ' Peryton version: ' + __version__
info_out(msg)
if MPI.COMM_WORLD.Get_rank() == 0:
    if 'peryton/__init__.pyc' in __file__:
        get_dir = __file__.replace('peryton/__init__.pyc', '.git')
    elif 'peryton/__init__.py' in __file__:
        get_dir = __file__.replace('peryton/__init__.py', '.git')
    try: label = subprocess.check_output(['git', '--git-dir='+get_dir, 'rev-parse', 'HEAD'])
    except: label = 'Could not retrieve git hash code'
    info_out('Installation hash code: ' + label)
    info_out('Installation location: {}\n'.format(__file__))


# Make firedrake (or COFFEE really) a little less chatty
set_log_level('CRITICAL')
