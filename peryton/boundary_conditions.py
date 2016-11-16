"""
.. module:: boundary_conditions
   :synopsis: Creates boundary conditions (strong dirichlet only)

"""

from firedrake import *
from helpers import info_out

class NS_BoundaryConditions(object):
    """ This class holds the strong Dirichlet boundary conditions for
    Navier-Stokes solves.
    """

    def __init__(self):
        self.bc_u_list = []
        self.bc_p_list = []
        self.domain = None
        # Keep a list of the boundary conditions that have been set
        self.list_of_bcs_set = []


    def _diagnose_input(self, bc_list, expression, facet_id, time_dependent):
        """ Looks at what has been passed in and appends to the specified
        boundary condition list appropriately
        """
        # If a float or int has been passed instead of an expression
        if isinstance(expression, int) or isinstance(expression, float):
            expression = Constant(expression)

        # If a list of facets have been passed in for the condition to be
        # applied to
        if isinstance(facet_id, list):
            for facet in facet_id:
                bc_list.append([expression, facet, time_dependent])
        else:
            bc_list.append([expression, facet_id, time_dependent])


    def add_bc_u(self, expression, facet_id, time_dependent=False):
        """ List of velocity boundary conditions' parameters

        :param expression: The expression for the bc to be applied
        :type expression: :class:`firedrake.expression`
        :param facet_id: The id number of the facet on which it's to be applied
        :type facet_id: int
        """
        self._diagnose_input(self.bc_u_list, expression, facet_id, time_dependent)


    def add_bc_p(self, expression=None, facet_id=None, time_dependent=False):
        """ List of pressure boundary conditions' parameters

        :param expression: The expression for the bc to be applied
        :type expression: :class:`firedrake.expression`
        :param facet_id: The id number of the facet on which it's to be applied
        :type facet_id: int
        """
        self._diagnose_input(self.bc_p_list, expression, facet_id, time_dependent)
