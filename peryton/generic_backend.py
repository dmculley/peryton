"""
.. :module: generic_backend
   .synopsis: Provides general backend functionality for all algorithms

"""

from firedrake import *
from helpers import *
import os
import sys
import time

class GenericBackendParameters(FrozenClass):

    output_dir = os.getcwd() + '/' + 'out_' + sys.argv[0][:-3] + '_on{0}_at{1}'\
                 .format(time.strftime("%d%m"), time.strftime("%H%M"))
    output_file = 'output.pvd'
    dump_period = 0


class GenericBackend(object):
    """ Provides generic backend functionality for all algorithms
    """

    def __init__(self, parameters, problem):

        self.params = parameters
        self.problem = problem

        self.params.output_file = File(self.params.output_dir \
                                       + self.params.output_file)

    def apply_initial_conditions(self):

        for function in self.params.parameter_dictionary.keys():
            if function in self.ics.keys():
                for field in self.diagnostic_functions[function]:
                    field.interpolate(self.ics.initial_conditions[function])
