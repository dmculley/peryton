"""
.. module:: initial_conditions
   :synopsis: Container holding the initial conditions

"""

from firedrake import *
from helpers import info_out


class NS_InitialConditions(object):
   """ Holds the initial conditions for Navier-Stokes solves -- i.e. for
    velocity and pressure

    Users can pass a :class:`firedrake.expression`, :class:`firedrake.function`
    or float.
    """

    def __init__(self, domain):
        self.n_dims = domain.n_dims
        self._get_default_ns_ics(n_dims)


    def _get_default_ns_ics(self, n_dims):
        if n_dims == 2:
            self.ic_u = Constant((0, 0))
        else:
            self.ic_u = Constant((0, 0, 0))

        self.ic_p = Constant(0)


    def process_initial_conditions(self):
        """ Turns the ics into a dictionary for easy application.
        """
        self.initial_conditions = {'u': self.ic_u,
                                   'p': self.ic_p}


    def _diagnose_input(self, value):
        if isinstance(value, float) or isinstance(value, int):
            return Constant(value)
        elif isinstance(value, constant.Constant):
            return value
        else:
            raise TypeError, "Initial condition must be float, int or Constant"


    def set_ic_u(self, value):
        self.ic_u = self._diagnose_input(value)


    def set_ic_p(self, value):
        self.ic_p = self._diagnose_input(value)

