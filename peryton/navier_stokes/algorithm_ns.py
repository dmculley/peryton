"""
.. module: algorithm_ns
   :synopsis: Implementation of the XXX algorithm for solving the navier stokes
   equations.

"""

from firedrake import *
from ..helpers import *
from backend_ns import NS_Backend, NS_BackendParameters

class NS_AlgorithmParameters(NS_BackendParameters):

    pass


class NS_Algorithm(NS_Backend):
    """ Implementations of the XXX algorithm for solving the navier stokes
    equations.
    """

    def __init__(self, parameters, problem):

        # Initialise the base class
        super(NS_Algorithm, self).__init__(parameters, problem)

        self.params = parameters
        self.problem = problem


    @staticmethod
    def default_parameters():
        """ Returns an instance of the default parameters set
        """
        return NS_AlgorithmParameters


    def run(self):
        """ Runs the XXX algorithm
        """

        # Set initial conditions
        self.apply_intial_conditions()

        # Apply boundary conditions
        self.apply_boundary_conditions()

        # Write ICs to file


        # Begin iterating
