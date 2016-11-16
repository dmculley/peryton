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
    output_frequency = 0


class GenericBackend(object):
    """ Provides generic backend functionality for all algorithms
    """

    def __init__(self, parameters, problem):

        self.params = parameters
        self.problem = problem
        self.ics = problem.params.ics
        self.bcs = problem.params.bcs

        self.dt = problem.params.dt
        self.Dt = Constant(self.dt)
        self.t = 0
        self.it_no = 0

        self.params.output_file = File(self.params.output_dir \
                                       + self.params.output_file)


    def apply_initial_conditions(self):
        """ Applys the initital conditions to the diagnositc fields.
        """
        self.ics.process_initial_conditions()
        for function in self.params.parameter_dictionary.keys():
            if function in self.ics.keys():
                function.interpolate(self.ics.initial_conditions[function])


    def apply_boundary_conditions(self):
        """ Applys the boundary conditions.
        """
        for function in self.params.parameter_dictionary.keys():
            if function in self.bcs.keys():
                for condition in self.bcs[function]
                    function.apply(condition)


    def dump_to_file(self):
        """ Dumps the solution prognostic and diagnostic fields to .pvd file.
        """
        output_file = self.params.output_file
        # TODO there must be a way to work out what to write based on the param
        # dict - but I can't work out how with the 'write' api.
        temp_str = 'output_file.write('
        for func in self.params.diagnostic_functions.keys():
            temp_str += func + ', '
        temp_str += 'time={})'.format(self.t)
        exec(temp_str)



