"""
.. example:: 01_laminar_diffusor
   :synopsis: A two dimensional diffusor at Re = 100

"""

from peryton import *
from scipy.special import erf

# Generate diffusor mesh
def dy(x, N=6.):
    return (erf(x - Lx/2.) + N)/(N - 1.)
Lx = 16
Ly = 1
resolution = 0.05
Nx = int(Lx * (1./resolution))
Ny = int(Ly * (1./resolution))
mesh = RectangleMesh(Nx, Ny, Lx, Ly)
x = mesh.coordinates.vector().dat.data[:]
x[:, 1] = x[:, 1] * dy(x[:, 0])

# Get the default parameter set for the problem
problem_parameters = Problem.default_parameters()

# Set up the domain
domain = SimpleDomain(mesh)
problem_parameters.domain = domain
domain.label_facet(1, 'Inflow', inlet=True)
domain.label_facet(2, 'Outlet', outlet=True)
domain.label_facet(3, 'Straight side wall', wall=True)
domain.label_facet(4, 'Diffusor wall', wall=True)

# Compute the inflow velocity
prescribed_reynolds_number = 100.
step_height                = Ly
nu                         = 1.81e-5
u_in                       = prescribed_reynolds_number * nu / step_height

# Boundary conditions
bcs = NS_BoundaryConditions()
bcs.add_bc_p(Constant(0), 2)
bcs.add_bc_u(Constant((u_in, 0)), 1)
bcs.add_bc_u(Constant((0, 0)), [3, 4])
problem_parameters.bcs = bcs

# Initial conditions
ics = NS_InitialConditions()
ics.set_ic_u = Constant((0, 0))
ics.set_ic_p = Constant(0)
problem_parameters.ics = ics

# Finish setting up the problem
problem_parameters.body_forces = Constant((0, 0))
problem_parameters.max_iterations = 10
problem_parameters.dt = 1
problem = Problem(problem_parameters)

# Get the default parameter set for the algorithm
algorithm_parameters = NS_Algorithm.default_parameters()

# Finish setting up the algorithm
algorithm_parameters.dump_period = 1
algorithm = NS_Algorithm(algorithm_parameters, problem)

# And set it running
algorithm.run()











