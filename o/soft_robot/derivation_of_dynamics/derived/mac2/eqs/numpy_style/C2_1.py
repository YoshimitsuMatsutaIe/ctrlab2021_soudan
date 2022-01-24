import numpy
def f(q, q_dot, xi):
    l1, l2, l3 = q[0,0], q[1,0], q[2,0]
    l1_dot, l2_dot, l3_dot = q_dot[0,0], q_dot[1,0], q_dot[2,0]

    return l1_dot*(1.38654137505663e-11*l1 + 5.72153164875459e-12*l2 - 1.96418867892903e-11*l3 + 8.32613864009457e-15) - l2_dot*(1.2466152575692e-11*l1 - 2.06113736247302e-11*l2 + 8.05356093237194e-12*l3 + 1.40368182567312e-14) + l3_dot*(5.69132167691212e-12*l1 + 2.33986794159514e-12*l2 - 8.05356093237194e-12*l3 + 3.44885608466901e-15)