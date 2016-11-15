"""
.. module:: helpers
   :synopsis: This module holds various helper functions and classes. These are
    mostly related to computational housekeeping rather than anything directly
    modelling related.

"""

from firedrake import *
from collections import namedtuple
from mpi4py import MPI
from pyop2.profiling import timed_stage


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   I N P U T   /   O U T P U T   F U N C T I O N S   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

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


# # # # # # # # # # # # # # # # # # # # # # # #
#   F I R E D R A K E   E X T E N S I O N S   #
# # # # # # # # # # # # # # # # # # # # # # # #

def pointwise_norm(function):
    """ Pointwise norm (rather than the integral of the L2norm over the
    domain as is returned by Firedrake.norm()
    """
    return sqrt(inner(function, function))


def tensor_jump(vector_field, normal):
    """ Equivalent of jump(scalar, n) for vectorial quantities. The
    inbuilt firedrake jump(vector, n) is as below but uses inner - i.e.
    returning a scalar... this here returns a vector.
    """
    return outer(vector_field('+'), normal('+')) \
    + outer(vector_field('-'), normal('-'))


ElementContinuity = namedtuple("ElementContinuity",
                               ["dg", "horizontal_dg", "vertical_dg"])
"""A named tuple describing the continuity of an element."""


def element_continuity(fiat_element):
    """Return an :class:`ElementContinuity` instance with the
    continuity of a given element.
    :arg fiat_element: The fiat element to determine the continuity
        of.
    :returns: A new :class:`ElementContinuity` instance.
    """
    import FIAT
    cell = fiat_element.get_reference_element()


    if isinstance(cell, FIAT.reference_element.TensorProductCell):
        # Pull apart
        horiz = element_continuity(fiat_element.A).dg
        vert = element_continuity(fiat_element.B).dg
        return ElementContinuity(dg=horiz and vert,
                                 horizontal_dg=horiz,
                                 vertical_dg=vert)
    else:
        edofs = fiat_element.entity_dofs()
        dim = cell.get_spatial_dimension()
        dg = True
        for i in range(dim - 1):
            if any(len(k) for k in edofs[i].values()):
                dg = False
                break
        return ElementContinuity(dg, dg, dg)


def defined_on_dg_function_space(function):
    """ Test whether the provided function is defined on a discontinuous
    functionspace (and return true if it is).
    """
    return element_continuity(function.function_space().fiat_element).dg


def get_function_space_degree(function):
    """ Get the degree of the functionspace on which the provided function is
    defined.
    """
    return function.function_space().ufl_element().degree()


def get_function_space(function):
    """ Return a tuple of CG / DG and the element degree for the functionspace
    upon which the provided element is defined.
    """
    fs = ['CG']
    if defined_on_dg_function_space(function):
        fs[0] = 'DG'
    fs.append(get_function_space_degree(function))
    return fs


# # # # # # # # # # #
# P R O F I L I N G #
# # # # # # # # # # #

def profile(func):
    """ Decorator to automatically label stages for the pyopt profiler
    """
    def func_wrapper(*args, **kwargs):
        with timed_stage('{}'.format(func.__name__[:15])):
            return func(*args, **kwargs)
    return func_wrapper


# # # # # # # # # # # # # # # # # # # # #
#   P Y T H O N   E X T E N S I O N S   #
# # # # # # # # # # # # # # # # # # # # #

def import_path(fullpath):
    """
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do.
    """
    # TODO check this out and see if it works
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    reload(module) # Might be out of date
    del sys.path[-1]
    return module


class FrozenClass(object):
    """ A class which can be (un-)frozen. If the class is frozen, no attributes
        can be added to the class. """

    __isfrozen = True

    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError("\n%r is a frozen class. \n%r is not a valid" \
                            " attribute.\n" % (self, key))

        object.__setattr__(self, key, value)

    def _freeze(self):
        """ Disallows adding new attributes. """
        self.__isfrozen = True

    def _unfreeze(self):
        """ Allows adding new attributes. """
        self.__isfrozen = False

    def _convert_type(self, k):
        attr = getattr(self, k)

        if isinstance(attr, bool):
            return attr
        try:
            return float(attr)
        except:
            return str(attr)

    def __str__(self):
        attrs = dir(self)
        attrs_dict = {}

        for k in attrs:
            if k.startswith("_"):
                continue
            val = self._convert_type(k)
            attrs_dict[k] = val

        return yaml.dump(attrs_dict, default_flow_style=False)
