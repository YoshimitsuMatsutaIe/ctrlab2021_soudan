import numpy as np

import C
import G
import M


q_large = np.array([[0.01, 0.01, 0.0]]).T
q_dot_large = np.array([[0.001, 0.001, 0.001]]).T
q_dot_dot_large = np.array([[0.001, 0.001, 0.01]]).T
xi_large = np.array([[1, 1, 1]]).T


tau = M.f(q_large, xi_large, q_dot_large) @ q_dot_dot_large +\
    C.f(q_large, xi_large, q_dot_large) @ q_dot_large +\
        G.f(q_large, xi_large, q_dot_large)

print(tau)