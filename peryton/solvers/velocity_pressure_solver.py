"""
.. module:: velocity_pressure_solver
   :synopsis: A module holding the forms, problem and solver for the velocity /
    pressure equations.

"""

from firedrake import *
from ..helpers import *


class VelocityPressureSolver(object):
    """ A class holding the forms, problem and solver for the velocity /
    pressure equations.
    """

    def __init__(self, domain, velocity_function_space, pressure_function_space,
                 boundary_conditions, body_forces, background_viscosity,
                 turbulent_viscosity=Constant(0), solver_params='direct'):

        self.domain = domain
        self.mesh = domain.mesh
        self.V = velocity_function_space
        self.Q = pressure_function_space
        self.bcs = boundary_conditions
        self.body_forces = body_forces
        self.nu_bg = background_viscosity
        self.nu_T = turbulent_viscosity
        self.solver_params = solver_params


    def get_solvers(self):
        """ Makes the linear variational solvers for the velocity / pressure
        solve.
        """
        # Get the problem
        self.get_problems()
        # Get the solver parameters
        self.get_petsc_params()
        # Define the solver
        self.solver = LinearVariationalSolver(self.problem,
                                            solver_parameters=self.petsc_params,
                                            options_prefix='TODO_')


    def get_problems(self):
        """ Makes the linear variational problems for the velocity / pressure
        solve.
        """
        # Get the variational forms of the equations
        self.get_forms()
        # Define the problem
        self.problem = LinearVariationalProblem(lhs_a, rhs_L, soln_placeholder,
                                                constant_jacobian=False)


    def get_forms(self):
        """ Make the variational forms for the velocity / pressure solve.
        """
        pass

    def get_petsc_params(self):
        """
        """
        pass
