"""
.. module: backend_ns
   :synopsis: backend functionality for the navier stokes algorithm

"""

from firedrake import *
from ../helpers import *
from ../generic_backend import *

class BackendNSParameters(GenericBackendParameters):

    variable_dictionary = {'u': 'Velocity',
                           'p': 'Pressure'}


class BackendNS(GenericBackend):
    """ Provides backend functionality specific to the Navier Stokes solver.
    """

    def __init__(self, parameters, problem):

        self.params = parameters
        self.problem = problem
        self.mesh = problem.domain.mesh

        # Set up the function spaces for velocity and pressure
        self.V = VectorFunctionSpace(self.mesh, 'CG', 2)
        self.Q = FunctionSpace(self.mesh, 'CG', 1)


    @staticmethod
    def default_parameters():
        """ Returns an instance of the default parameters set
        """
        return BackendNSParameters()


    def initialise_functions(self):
        """ Make the functions for solutions and quantities
        """
        mesh = self.mesh

        # Velocity functions
        self.u_n       = Function(self.V, name='u_n')
        self.u_nminus1 = Function(self.V, name='u_nminus1')

        # Pressure functions
        self.p_n       = Function(self.Q, name='p_n')
        self.p_nminus1 = Function(self.Q, name='p_nminus1')

        # Store the functions in a dictionary for convenience
        self.diagnostic_variables = {'u': [self.u_n, self.u_nminus1],
                                     'p': [self.p_n, self.p_nminus1]}

