"""
.. module:: problem
   :synopsis: Object for setting up the problem to be solved

"""

class ProblemParameters(FrozenClass):
    """
    """

    # Physical constants
    rho   = 1.1766
    nu    = 1.81e-5

    # Forcing
    body_forces = None

    # Boundary and initial conditions
    bcs = None
    ics = None

    # Maximum iterations (pseudo-timesteps)
    max_iterations = 200

    # Problem domain
    domain = None


class Problem(object):
    """
    """

    def __init__(self, parameters):

        self.params = parameters

        if not self.params.body_forces:
            if self.params.domain.n_dims == 2:
                self.params.body_forces = Constant((0, 0))
            else:
                self.params.body_forces = Constant((0, 0, 0))


    @staticmethod
    def default_parameters():
        return ProblemParameters()





