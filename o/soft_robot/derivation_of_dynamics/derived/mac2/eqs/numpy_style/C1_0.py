import numpy
def f(q, q_dot, xi):
    l1, l2, l3 = q[0,0], q[1,0], q[2,0]
    l1_dot, l2_dot, l3_dot = q_dot[0,0], q_dot[1,0], q_dot[2,0]

    return -l1_dot*(5.51654750651859e-11*l1 - 3.38058845865336e-11*l2 - 2.16714051041859e-11*l3 + 4.74559579421492e-14) + l2_dot*(3.38058845865336e-11*l1 - 4.28998384220961e-11*l2 + 8.86717956244728e-12*l3 + 3.48300489468293e-14) + l3_dot*(2.16714051041859e-11*l1 + 8.86717956244728e-12*l2 - 3.06236268282961e-11*l3 + 1.31758393214915e-14)