"""
.. module:: domain
   :synopsis: Object to hold the domain-related info together

"""

import os.path
from firedrake import *

class PrototypeDomain(object):
    """ An prototypical domain class.
    """

    def __init__(self):
        raise NotImplementedError("Domain is a base class only.")

    def __str__(self):
        hmin = 'NOT IMPLEMENTED'
        hmax = 'NOT IMPLEMENTED'
        num_cells = self.mesh.topology.num_cells()

        s = "Number of mesh elements: {}.\n".format(num_cells)
        s += "Mesh element size: {1} - {2}.".format(hmin, hmax)

        return s

    def label_facet(self, facet, label, inlet=False, outlet=False, wall=False,
                    free_slip_boundary=False):
        """ Add a label to the facets

        Labelling can be done in one shot with `domain.facet_labels = {facet id
        number (str): label (str)...}`. The list of wall facets can also be set
        with `domain.wall_list = [1, 2, ...]`.

        :param facet: The numerical facet label from the mesh
        :type mesh_file: int
        :param label: The human label for the facet
        :type mesh_file: str
        :param inlet: Specify if facet represents a inlet
        :type inlet: bool
        :param outlet: Specify if facet represents a outlet
        :type outlet: bool
        :param wall: Specify if facet represents a wall
        :type wall: bool
        :param free_slip_boundary: Specify if facet represents a free-slip boundary
        :type wall: bool

        """
        if not isinstance(facet, list): facet = [facet]
        for f in facet:
            self.facet_labels[str(f)] = label
            if inlet:
                self.inlet_list.append(f)
            if outlet:
                self.outlet_list.append(f)
            if wall:
                self.wall_list.append(f)
            if free_slip_boundary:
                self.free_slip_boundary_list.append(f)


class FileDomain(PrototypeDomain):
    """ Create a domain from a mesh file (.msh).

    :param mesh_file: The .msh file of the mesh.
    :type mesh_file: str

    """

    def __init__(self, mesh_file):

        self.mesh = Mesh(mesh_file)
        # Stores string facet labels against their id number
        self.facet_labels = {}
        # Create a list of boundary types
        self.inlet_list = []
        self.outlet_list = []
        self.wall_list = []
        self.free_slip_boundary_list = []
        self.n_dims = self.mesh.geometric_dimension()


class SimpleDomain(PrototypeDomain):
    """ Create a domain from a firedrake Mesh object.

    :param mesh: The mesh object.
    :type mesh_file: firedrake.Mesh

    """

    def __init__(self, mesh):

        self.mesh = mesh
        # Stores string facet labels against their id number
        self.facet_labels = {}
        # Create lists of boundary types
        self.inlet_list = []
        self.outlet_list = []
        self.wall_list = []
        self.free_slip_boundary_list = []
        self.n_dims = self.mesh.geometric_dimension()


